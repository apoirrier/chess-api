from fastapi import APIRouter

from app.schemas.requests import EvaluatePlayerMoveRequest
from app.schemas.responses import FeedbackResponse
from app.services.feedback_service import evaluate_player_move

router = APIRouter(
    prefix="/feedback",
    tags=["Feedback"],
)


@router.post(
    "/evaluate",
    response_model=FeedbackResponse,
)
def evaluate(request: EvaluatePlayerMoveRequest):
    feedback = evaluate_player_move(
        request.before,
        request.move,
    )
    return FeedbackResponse(feedback=feedback)
