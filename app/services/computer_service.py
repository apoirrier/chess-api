import datetime
import io
import random

import chess
import chess.pgn
from sqlalchemy import func, select, update

from app.db.models import ComputerMove, Position
from app.db.session import SessionLocal
from app.schemas.responses import Status
from app.services.chess import epd_from_fen


def play_computer_move(fen: str) -> tuple[str, str]:
    epd = epd_from_fen(fen)
    move = ""
    message = ""
    with SessionLocal() as session:
        position = session.scalar(
            select(Position).where(Position.epd == epd)
        )
        if position and len(position.computer_moves) > 0:
            oldest_date_query = select(func.min(ComputerMove.next_repetition)).where(
                ComputerMove.position_id == position.id
            )
            moves = session.scalars(
                select(ComputerMove).where(
                    ComputerMove.position_id == position.id,
                    ComputerMove.next_repetition == oldest_date_query.scalar_subquery()
                )
            ).all()
            random_move = random.choice(moves)
            move = random_move.move
            message = random_move.message
    return move, message

def _today_plus_n(n: int):
    return datetime.date.today() + datetime.timedelta(days=n) # noqa: DTZ011

def _next_bucket(bucket: int):
    if bucket <= 1:
        return 3
    elif bucket == 3:
        return 7
    elif bucket == 7:
        return 14
    else:
        return 30

def _update_leaf(fen: str, san: str, error_made: bool) -> datetime.date:
    epd = epd_from_fen(fen)
    with SessionLocal() as session:
        position = session.scalar(
            select(Position).where(Position.epd == epd)
        )
        if not position:
            raise ValueError(f"Impossible de trouver la position {epd} dans la base de données")
        move = session.scalar(
            select(ComputerMove).where(
                ComputerMove.position_id == position.id,
                ComputerMove.move == san
            )
        )
        if not move:
            raise ValueError(f"Impossible de trouver le coup {san} pour la position {epd} dans la base de données")
        next_bucket = 1 if error_made else _next_bucket(move.repetition_bucket)
        next_date = _today_plus_n(next_bucket)
        session.execute(
            update(ComputerMove).where(
                ComputerMove.position_id == position.id,
                ComputerMove.move == san
            ).values(
                repetition_bucket=next_bucket,
                next_repetition=next_date
            )
        )
        session.commit()
        return next_date

def _update_next_repetition(fen: str, san: str, next_date: datetime.date):
    epd = epd_from_fen(fen)
    with SessionLocal() as session:
        position = session.scalar(
            select(Position).where(Position.epd == epd)
        )
        if not position:
            raise ValueError(f"Impossible de trouver la position {epd} dans la base de données")
        session.execute(
            update(ComputerMove).where(
                ComputerMove.position_id == position.id,
                ComputerMove.move == san
            ).values(
                next_repetition=next_date
            )
        )
        session.commit()

def _get_oldest_date(fen: str) -> datetime.date:
    epd = epd_from_fen(fen)
    with SessionLocal() as session:
        position = session.scalar(
            select(Position).where(Position.epd == epd)
        )
        if not position:
            raise ValueError(f"Impossible de trouver la position {epd} dans la base de données")
        oldest_date = session.scalar(
            select(func.min(ComputerMove.next_repetition)).where(
                ComputerMove.position_id == position.id
            )
        )
        if not oldest_date:
            raise ValueError(f"Impossible de trouver la plus vieille date pour la position {epd} dans la base de données")
        return oldest_date

def end_variation(pgn: str, error_made: bool, player_color: str) -> tuple[Status, str]:
    game = chess.pgn.read_game(io.StringIO(pgn))

    if game is None:
        return Status.ERROR, "Impossible de lire le PGN."

    player = chess.WHITE if player_color == "white" else chess.BLACK

    board = game.board()
    for move in game.mainline_moves():
        board.push(move)

    next_date = None

    while True:
        try:
            move = board.pop()
            if board.turn == player:
                continue

            if next_date is None:
                next_date = _update_leaf(board.fen(), board.san(move), error_made)
            else:
                _update_next_repetition(board.fen(), board.san(move), next_date)
            next_date = _get_oldest_date(board.fen())
        except IndexError:
            break
        except ValueError as e:
            return Status.ERROR, str(e)
    return Status.SUCCESS, "success"
