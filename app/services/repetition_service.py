import datetime

import chess
import chess.pgn
from sqlalchemy import func, select, update

from app.db.models import ComputerMove, Position
from app.db.session import SessionLocal
from app.services.chess import epd_from_fen


def _today_plus_n(n: int):
    return datetime.date.today() + datetime.timedelta(days=n)  # noqa: DTZ011


def _next_bucket(bucket: int):
    if bucket <= 1:
        return 3
    elif bucket == 3:
        return 7
    elif bucket == 7:
        return 14
    else:
        return 30


def _update_leaf(fen: str, san: str, default_bucket: int) -> datetime.date:
    epd = epd_from_fen(fen)
    with SessionLocal() as session:
        position = session.scalar(select(Position).where(Position.epd == epd))
        if not position:
            raise ValueError(
                f"Impossible de trouver la position {epd} dans la base de données"
            )
        move = session.scalar(
            select(ComputerMove).where(
                ComputerMove.position_id == position.id, ComputerMove.move == san
            )
        )
        if not move:
            raise ValueError(
                f"Impossible de trouver le coup {san} pour la position {epd} dans la base de données"
            )
        next_bucket = default_bucket
        if default_bucket < 0:
            next_bucket = _next_bucket(move.repetition_bucket)
        next_date = _today_plus_n(next_bucket)
        session.execute(
            update(ComputerMove)
            .where(ComputerMove.position_id == position.id, ComputerMove.move == san)
            .values(repetition_bucket=next_bucket, next_repetition=next_date)
        )
        session.commit()
        return next_date


def _update_next_repetition(fen: str, san: str, next_date: datetime.date):
    epd = epd_from_fen(fen)
    with SessionLocal() as session:
        position = session.scalar(select(Position).where(Position.epd == epd))
        if not position:
            raise ValueError(
                f"Impossible de trouver la position {epd} dans la base de données"
            )
        session.execute(
            update(ComputerMove)
            .where(ComputerMove.position_id == position.id, ComputerMove.move == san)
            .values(next_repetition=next_date)
        )
        session.commit()


def _get_oldest_date(fen: str) -> datetime.date:
    epd = epd_from_fen(fen)
    with SessionLocal() as session:
        position = session.scalar(select(Position).where(Position.epd == epd))
        if not position:
            raise ValueError(
                f"Impossible de trouver la position {epd} dans la base de données"
            )
        oldest_date = session.scalar(
            select(func.min(ComputerMove.next_repetition)).where(
                ComputerMove.position_id == position.id
            )
        )
        if not oldest_date:
            raise ValueError(
                f"Impossible de trouver la plus vieille date pour la position {epd} dans la base de données"
            )
        return oldest_date


def backpropagate(board: chess.Board, player: chess.Color, default_bucket: int):
    next_date = None
    while True:
        try:
            move = board.pop()
            if board.turn == player:
                continue

            if next_date is None:
                next_date = _update_leaf(board.fen(), board.san(move), default_bucket)
            else:
                _update_next_repetition(board.fen(), board.san(move), next_date)
            next_date = _get_oldest_date(board.fen())
        except IndexError:
            break
