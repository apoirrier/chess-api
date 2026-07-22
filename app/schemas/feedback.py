from app.common.feedback_type import FeedbackType
from pydantic import BaseModel

class Feedback(BaseModel):
    type: FeedbackType
    message: str | None = None
