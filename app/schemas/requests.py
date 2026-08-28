from pydantic import BaseModel


class PlayComputerMoveRequest(BaseModel):
    fen: str


class EvaluatePlayerMoveRequest(BaseModel):
    before: str
    move: str


class ImportPGNRequest(BaseModel):
    pgn: str


class OpeningNameRequest(BaseModel):
    fen: str


class EndVariationRequest(BaseModel):
    pgn: str
    errorMade: bool
    playerColor: str
