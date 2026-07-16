def extract_position_from_fen(fen: str) -> str:
    return " ".join(fen.split()[:2])
