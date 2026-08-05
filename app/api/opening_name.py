from fastapi import APIRouter

from app.schemas.requests import OpeningNameRequest
from app.schemas.responses import OpeningNameResponse
from app.services.opening_name_service import get_opening_name

router = APIRouter(
    prefix="/opening-name",
    tags=["Opening Name"],
)


@router.post(
    "",
    response_model=OpeningNameResponse,
)
def opening(request: OpeningNameRequest):
    opening_name = get_opening_name(
        request.fen,
    )
    return OpeningNameResponse(name=opening_name)
