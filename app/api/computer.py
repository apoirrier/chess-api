from fastapi import APIRouter

from app.schemas.requests import PlayComputerMoveRequest
from app.schemas.responses import PlayComputerMoveResponse
from app.services.computer_service import play_computer_move

router = APIRouter(
    prefix="/computer",
    tags=["Computer"],
)


@router.post(
    "/play",
    response_model=PlayComputerMoveResponse,
)
def play_move(request: PlayComputerMoveRequest):
    return play_computer_move(request.fen)