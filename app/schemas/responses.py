from pydantic import BaseModel
from feedback import Feedback

class PlayComputerMoveResponse(BaseModel):
    move: str

class FeedbackResponse(BaseModel):
    feedback: Feedback