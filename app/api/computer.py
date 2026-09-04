from fastapi import APIRouter

from app.api.deps import CurrentUser
from app.schemas.requests import EndVariationRequest, PlayComputerMoveRequest
from app.schemas.responses import BasicResponse, PlayComputerMoveResponse
from app.services.computer_service import end_variation, play_computer_move

router = APIRouter(
    prefix="/computer",
    tags=["Computer"],
)


@router.post(
    "/play",
    response_model=PlayComputerMoveResponse,
)
def play_move(request: PlayComputerMoveRequest, user: CurrentUser):
    move, message, date = play_computer_move(request.fen)
    return PlayComputerMoveResponse(move=move, message=message, date=date)


@router.post(
    "/end-variation",
    response_model=BasicResponse,
)
def end_variation_route(request: EndVariationRequest, user: CurrentUser):
    status, message = end_variation(request.pgn, request.errorMade, request.playerColor)
    return BasicResponse(status=status, message=message)
