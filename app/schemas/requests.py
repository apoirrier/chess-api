from pydantic import BaseModel


class PlayComputerMoveRequest(BaseModel):
    fen: str


class EvaluatePlayerMoveRequest(BaseModel):
    fen: str
    move: str