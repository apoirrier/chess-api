import io

import chess
import chess.pgn
from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert

from app.db.models import ComputerMove, Position
from app.db.models import Feedback as FeedbackDB
from app.db.session import SessionLocal
from app.schemas.feedback_type import FeedbackType
from app.services.chess import epd_from_fen, get_color_from_epd
from app.services.repetition_service import backpropagate


def add_computer_move(before: str, move: str, comment: str) -> bool:
    with SessionLocal() as session:
        stmt = (
            insert(Position)
            .values(epd=before)
            .on_conflict_do_nothing(index_elements=["epd"])
        )
        session.execute(stmt)

        position = session.scalar(select(Position).where(Position.epd == before))
        if position is None:
            raise ValueError("Une erreur de base de données est survenue.")

        stmt = (
            insert(ComputerMove)
            .values(move=move, message=comment, position_id=position.id)
            .on_conflict_do_nothing(constraint="uq_position_move")
            .returning(ComputerMove.id)
        )
        inserted_id = session.execute(stmt).scalar_one_or_none()
        session.commit()
        return inserted_id is not None


def add_player_move(before: str, move: str, comment: str):
    feedback_type = FeedbackType.SUCCESS
    if "cls:green" in comment or "cls:orange" in comment:
        feedback_type = FeedbackType.NOBEST
        comment = comment.replace("cls:green ", "")
        comment = comment.replace("cls:orange ", "")
    elif "cls:red" in comment:
        feedback_type = FeedbackType.ERROR
        comment = comment.replace("cls:red ", "")

    with SessionLocal() as session:
        stmt = (
            insert(FeedbackDB)
            .values(
                epd=before,
                move=move,
                type=feedback_type,
                message=comment,
            )
            .on_conflict_do_update(
                constraint="uq_epd_move",
                set_={
                    "type": feedback_type,
                    "message": comment,
                },
            )
        )
        session.execute(stmt)
        session.commit()


def process_move(before: str, move: str, comment: str, player: str) -> bool:
    if get_color_from_epd(before) == player:
        add_player_move(before, move, comment)
        return False  # By default, we'll say new human moves are not new moves
    else:
        return add_computer_move(before, move, comment)


def browse_pgn(
    node: chess.pgn.GameNode, board: chess.Board, player: str, new_variation=False
):
    before = epd_from_fen(board.fen())
    new_board = chess.Board(before)

    if node.move is not None:
        new_board.push(node.move)
        is_new_variation = process_move(
            before, board.san(node.move), node.comment, player
        )
        new_variation = new_variation or is_new_variation

    for variation in node.variations:
        browse_pgn(variation, new_board, player, new_variation)

    if len(node.variations) == 0 and new_variation:
        backpropagate(new_board, chess.WHITE if player == "w" else chess.BLACK, 0)


def import_pgn(pgn: str):
    game = chess.pgn.read_game(io.StringIO(pgn))

    if game is None:
        raise ValueError("Impossible d'importer le PGN.")

    if "blanc" in game.headers["ChapterName"].lower():
        player = "w"
    elif "noir" in game.headers["ChapterName"].lower():
        player = "b"
    else:
        raise ValueError("Couleur du joueur introuvable.")

    board = game.board()
    browse_pgn(game, board, player)
