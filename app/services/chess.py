def epd_from_fen(fen: str) -> str:
    return " ".join(fen.strip().split()[:4])

def get_color_from_epd(epd: str) -> str:
    return epd.split()[1]