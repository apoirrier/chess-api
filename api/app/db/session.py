import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL_FILE = os.environ.get("DATABASE_URL_FILE", "/run/secrets/db_url")
DATABASE_URL = open(DATABASE_URL_FILE, "r").read().strip()

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)
