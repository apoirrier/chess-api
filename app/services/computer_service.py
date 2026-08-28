import io
import random

import chess
import chess.pgn
from sqlalchemy import func, select

from app.db.models import ComputerMove, Position
from app.db.session import SessionLocal
from app.schemas.responses import Status
from app.services.chess import epd_from_fen
from app.services.repetition_service import backpropagate


def play_computer_move(fen: str) -> tuple[str, str]:
    epd = epd_from_fen(fen)
    move = ""
    message = ""
    with SessionLocal() as session:
        position = session.scalar(select(Position).where(Position.epd == epd))
        if position and len(position.computer_moves) > 0:
            oldest_date_query = select(func.min(ComputerMove.next_repetition)).where(
                ComputerMove.position_id == position.id
            )
            moves = session.scalars(
                select(ComputerMove).where(
                    ComputerMove.position_id == position.id,
                    ComputerMove.next_repetition == oldest_date_query.scalar_subquery(),
                )
            ).all()
            random_move = random.choice(moves)
            move = random_move.move
            message = random_move.message
    return move, message


def end_variation(pgn: str, error_made: bool, player_color: str) -> tuple[Status, str]:
    game = chess.pgn.read_game(io.StringIO(pgn))

    if game is None:
        return Status.ERROR, "Impossible de lire le PGN."

    player = chess.WHITE if player_color == "white" else chess.BLACK

    board = game.board()
    for move in game.mainline_moves():
        board.push(move)

    try:
        default_bucket = 1 if error_made else -1
        backpropagate(board, player, default_bucket)
    except ValueError as e:
        return Status.ERROR, str(e)
    return Status.SUCCESS, "success"
