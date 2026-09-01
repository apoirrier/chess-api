from sqlalchemy import select

from app.db.models import Feedback as FeedbackDB
from app.db.session import SessionLocal
from app.schemas.feedback import Feedback, bad_feedback
from app.schemas.feedback_type import FeedbackType
from app.services.chess import epd_from_fen, uci_from_san


def evaluate_player_move(
    before: str,
    move: str,
) -> Feedback:
    epd = epd_from_fen(before)
    feedback = bad_feedback
    with SessionLocal() as session:
        feedback_db = session.scalar(
            select(FeedbackDB).where(FeedbackDB.epd == epd, FeedbackDB.move == move)
        )

        if feedback_db:
            feedback = Feedback(type=feedback_db.type, message=feedback_db.message)

        if feedback.type == FeedbackType.ERROR:
            solution = session.scalar(
                select(FeedbackDB.move).where(FeedbackDB.epd == epd, FeedbackDB.type == FeedbackType.SUCCESS)
            )
            if solution:
                feedback.solution = uci_from_san(solution, epd)

    return feedback
