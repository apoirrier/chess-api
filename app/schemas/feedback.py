from pydantic import BaseModel

from app.schemas.feedback_type import FeedbackType


class Feedback(BaseModel):
    type: FeedbackType
    message: str | None = None

good_feedback = Feedback(type=FeedbackType.SUCCESS, message="")
bad_feedback = Feedback(type=FeedbackType.ERROR, message="")