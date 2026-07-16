from app.schemas.responses import PlayComputerMoveResponse
from app.common.chess import extract_position_from_fen

def play_computer_move(fen: str) -> PlayComputerMoveResponse:
    position = extract_position_from_fen(fen)
    move = ""
    match position:
        case "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w":
            move="e4"
        case "rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR b":
            move="e5"
        case "rnbqkbnr/pp1ppppp/8/2p5/4P3/8/PPPP1PPP/RNBQKBNR w":
            move="Nf3"
    return PlayComputerMoveResponse(
        move=move
    )