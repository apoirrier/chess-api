import chess


def epd_from_fen(fen: str) -> str:
    return " ".join(fen.strip().split()[:4])


def get_color_from_epd(epd: str) -> str:
    return epd.split()[1]

def uci_from_san(san: str, epd: str) -> str:
    board = chess.Board()
    board.set_epd(epd)
    move = board.parse_san(san)
    return move.uci()