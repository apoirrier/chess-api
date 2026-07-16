from app.schemas.responses import PlayComputerMoveResponse

def play_computer_move(fen: str) -> PlayComputerMoveResponse:
    """
    Dummy implementation.

    Later this will:
    - find the position
    - choose a move
    - return it
    """

    return PlayComputerMoveResponse(
        move="Nf3"
    )