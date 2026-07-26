from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

if TYPE_CHECKING:
    from .position import Position


class ComputerMove(Base):
    __tablename__ = "computer_moves"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    move: Mapped[str] = mapped_column(String(10), nullable=False)
    message: Mapped[str] = mapped_column(String(200), nullable=False)
    position_id: Mapped[int] = mapped_column(ForeignKey("positions.id"), nullable=False)

    position: Mapped["Position"] = relationship(
        "Position",
        back_populates="computer_moves"
    )

    __table_args__ = (
        UniqueConstraint("position_id", "move", name="uq_position_move"),
    )