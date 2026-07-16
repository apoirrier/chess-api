from enum import Enum
from pydantic import BaseModel

class FeedbackType(str, Enum):
    IDLE = "idle"
    SUCCESS = "success"
    NOBEST = "nobest"
    ERROR = "error"

class Feedback(BaseModel):
    type: FeedbackType
    message: str | None = None
