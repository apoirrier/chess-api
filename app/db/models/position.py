from typing import TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

if TYPE_CHECKING:
    from .computer_move import ComputerMove


class Position(Base):
    __tablename__ = "positions"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    epd: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    opening_name: Mapped[str | None] = mapped_column(String(100), nullable=True)

    computer_moves: Mapped[list["ComputerMove"]] = relationship(
        "ComputerMove", back_populates="position"
    )
