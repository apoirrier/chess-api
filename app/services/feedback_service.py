from sqlalchemy import select

from app.common.chess import extract_position_from_fen
from app.db.models import Feedback as FeedbackDB
from app.db.session import SessionLocal
from app.schemas.feedback import Feedback, bad_feedback


def evaluate_player_move(
    before: str,
    move: str,
) -> Feedback:
    position = extract_position_from_fen(before)
    feedback = bad_feedback
    with SessionLocal() as session:
        feedback_db = session.scalar(
            select(FeedbackDB).where(
                FeedbackDB.fen == position,
                FeedbackDB.move == move
            )
        )
        if feedback_db:
            feedback = Feedback(
                type = feedback_db.type,
                message = feedback_db.message
            )

    return feedback
