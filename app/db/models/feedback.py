from sqlalchemy import Enum as SQLEnum, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from app.common.feedback_type import FeedbackType
from app.db.base import Base

class Feedback(Base):
    __tablename__ = "feedback"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    type: Mapped[FeedbackType] = mapped_column(SQLEnum(FeedbackType), nullable=False)
    message: Mapped[str | None] = mapped_column(String(200), nullable=True)
    move: Mapped[str] = mapped_column(String(10), nullable=False)
    position_id: Mapped[int] = mapped_column(ForeignKey("positions.id"), nullable=False)
