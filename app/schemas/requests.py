from pydantic import BaseModel

from app.schemas.player_color import PlayerColor


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
    playerColor: PlayerColor
