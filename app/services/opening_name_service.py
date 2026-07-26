from sqlalchemy import select

from app.common.chess import epd_from_fen
from app.db.models import Position
from app.db.session import SessionLocal


def get_opening_name(fen: str) -> str:
    epd = epd_from_fen(fen)
    opening_name = ""
    with SessionLocal() as session:
        position = session.scalar(
            select(Position).where(Position.epd == epd)
        )
        if position and position.opening_name is not None:
            opening_name = position.opening_name
    return opening_name