from enum import Enum

from pydantic import BaseModel

from app.schemas.feedback import Feedback
from app.schemas.player_color import PlayerColor


class Status(str, Enum):
    SUCCESS = "success"
    ERROR = "error"


class PlayerColorResponse(BaseModel):
    playerColor: PlayerColor


class PlayComputerMoveResponse(BaseModel):
    move: str
    message: str
    date: str | None = None


class FeedbackResponse(BaseModel):
    feedback: Feedback


class ImportPGNResponse(BaseModel):
    message: str


class OpeningNameResponse(BaseModel):
    name: str


class BasicResponse(BaseModel):
    status: Status
    message: str
