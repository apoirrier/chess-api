from app.schemas.responses import FeedbackResponse

def evaluate_player_move(
    fen: str,
    move: str,
) -> FeedbackResponse:
    """
    Dummy implementation.
    """

    return FeedbackResponse(
        quality="good",
        message="This move is part of the opening repertoire."
    )