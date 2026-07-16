from app.schemas.responses import FeedbackResponse
from app.common.chess import extract_position_from_fen
from common.feedback import good_feedback, bad_feedback, sicilian_feedback, french_feedback

def evaluate_player_move(
    before: str,
    move: str,
) -> FeedbackResponse:
    position = extract_position_from_fen(before)
    feedback = bad_feedback
    match position:
        case "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w":
            match move:
                case "e4":
                    feedback = good_feedback
                case _:
                    feedback = bad_feedback
        case "rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR b":
            match move:
                case "e6":
                    feedback = french_feedback
                case "c5":
                    feedback = sicilian_feedback
                case _:
                    feedback = bad_feedback
    return FeedbackResponse(
        feedback=feedback
    )