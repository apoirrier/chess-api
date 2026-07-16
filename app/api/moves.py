from fastapi import APIRouter

from app.schemas.requests import PlayComputerMoveRequest
from app.schemas.responses import PlayComputerMoveResponse
from app.services.move_service import play_computer_move

router = APIRouter(
    prefix="/moves",
    tags=["Moves"],
)


@router.post(
    "/play",
    response_model=PlayComputerMoveResponse,
)
def play_move(request: PlayComputerMoveRequest):
    return play_computer_move(request.fen)