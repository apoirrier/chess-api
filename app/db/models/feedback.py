from sqlalchemy import Enum as SQLEnum
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base
from app.schemas.feedback_type import FeedbackType


class Feedback(Base):
    __tablename__ = "feedback"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    type: Mapped[FeedbackType] = mapped_column(SQLEnum(FeedbackType), nullable=False)
    message: Mapped[str | None] = mapped_column(String(200), nullable=True)
    move: Mapped[str] = mapped_column(String(10), nullable=False)
    fen: Mapped[str] = mapped_column(String(100), nullable=False)
