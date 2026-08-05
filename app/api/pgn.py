from fastapi import APIRouter, HTTPException

from app.api.deps import CurrentUser
from app.schemas.requests import ImportPGNRequest
from app.schemas.responses import ImportPGNResponse
from app.services.pgn_service import import_pgn

router = APIRouter(
    prefix="/pgn",
    tags=["pgn"],
)


@router.post(
    "",
    response_model=ImportPGNResponse,
)
def pgn_import(request: ImportPGNRequest, user: CurrentUser):
    try:
        import_pgn(request.pgn)
        return ImportPGNResponse(message="success")
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )
