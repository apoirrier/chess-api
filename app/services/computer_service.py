import io
import random

import chess
import chess.pgn
from sqlalchemy import select

from app.db.models import ComputerMove, Position
from app.db.session import SessionLocal
from app.schemas.responses import PlayerColor, Status
from app.services.chess import epd_from_fen
from app.services.repetition_service import backpropagate, get_oldest_date_from_fen


def get_player_color() -> PlayerColor:
    # Colors are inverted because we are considering the computer move, not the player
    fen_black = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
    fen_white = "rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR b KQkq - 0 1"
    oldest_date_white = get_oldest_date_from_fen(fen_white)
    oldest_date_black = get_oldest_date_from_fen(fen_black)
    if oldest_date_white < oldest_date_black:
        return PlayerColor.WHITE
    elif oldest_date_black < oldest_date_white:
        return PlayerColor.BLACK
    return random.choice([PlayerColor.WHITE, PlayerColor.BLACK])


def play_computer_move(fen: str) -> tuple[str, str, str | None]:
    epd = epd_from_fen(fen)
    move = ""
    message = ""
    date = None
    with SessionLocal() as session:
        position = session.scalar(select(Position).where(Position.epd == epd))
        if position and len(position.computer_moves) > 0:
            oldest_date = get_oldest_date_from_fen(fen)
            moves = session.scalars(
                select(ComputerMove).where(
                    ComputerMove.position_id == position.id,
                    ComputerMove.next_repetition == oldest_date,
                )
            ).all()
            random_move = random.choice(moves)
            move = random_move.move
            message = random_move.message
            date = str(random_move.next_repetition)
    return move, message, date


def end_variation(pgn: str, error_made: bool, player_color: PlayerColor) -> tuple[Status, str]:
    game = chess.pgn.read_game(io.StringIO(pgn))

    if game is None:
        return Status.ERROR, "Impossible de lire le PGN."

    player = chess.WHITE if player_color == PlayerColor.WHITE else chess.BLACK

    board = game.board()
    for move in game.mainline_moves():
        board.push(move)

    try:
        default_bucket = 1 if error_made else -1
        backpropagate(board, player, default_bucket)
    except ValueError as e:
        return Status.ERROR, str(e)
    return Status.SUCCESS, "success"
