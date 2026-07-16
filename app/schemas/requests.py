from pydantic import BaseModel


class PlayComputerMoveRequest(BaseModel):
    fen: str


class EvaluatePlayerMoveRequest(BaseModel):
    before: str
    move: str
