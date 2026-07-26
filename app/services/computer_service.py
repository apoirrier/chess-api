import random

from sqlalchemy import select

from app.common.chess import epd_from_fen
from app.db.models import Position
from app.db.session import SessionLocal


def play_computer_move(fen: str) -> tuple[str, str]:
    epd = epd_from_fen(fen)
    move = ""
    message = ""
    with SessionLocal() as session:
        position = session.scalar(
            select(Position).where(Position.epd == epd)
        )
        if position and len(position.computer_moves) > 0:
            random_move = random.choice(position.computer_moves)
            move = random_move.move
            message = random_move.message
    return move, message