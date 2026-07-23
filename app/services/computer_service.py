import random

from sqlalchemy import select

from app.common.chess import extract_position_from_fen
from app.db.models import Position
from app.db.session import SessionLocal


def play_computer_move(fen: str) -> str:
    fen_position = extract_position_from_fen(fen)
    move = ""
    with SessionLocal() as session:
        position = session.scalar(
            select(Position).where(Position.fen == fen_position)
        )
        if position and len(position.computer_moves) > 0:
            random_move = random.choice(position.computer_moves)
            move = random_move.move
    return move