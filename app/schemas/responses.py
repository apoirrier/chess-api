from pydantic import BaseModel


class PlayComputerMoveResponse(BaseModel):
    move: str


class FeedbackResponse(BaseModel):
    quality: str
    message: str