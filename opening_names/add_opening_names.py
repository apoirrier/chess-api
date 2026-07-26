import csv
from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert

from app.db.models import Position
from app.db.session import SessionLocal

def add_opening_name_to_db(epd: str, name: str):
    with SessionLocal() as session:
        position = session.scalar(
            select(Position).where(Position.epd == epd)
        )
        if not position:
            stmt = insert(Position).values(
                epd=epd,
                opening_name=name,
            ).on_conflict_do_nothing(
                index_elements=["epd"]
            )
            session.execute(stmt)
        elif position and position.opening_name is None:
            position.opening_name = name
        session.commit()

def import_opening_names():
    with open("opening_names/all.tsv", "r", encoding="utf-8") as f:
        reader = csv.DictReader(f, delimiter="\t")
        for row in reader:
            add_opening_name_to_db(row["epd"], row["name"])

if __name__ == "__main__":
    import_opening_names()