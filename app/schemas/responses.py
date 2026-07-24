from pydantic import BaseModel

from app.schemas.feedback import Feedback


class PlayComputerMoveResponse(BaseModel):
    move: str


class FeedbackResponse(BaseModel):
    feedback: Feedback


class ImportPGNResponse(BaseModel):
    message: str
