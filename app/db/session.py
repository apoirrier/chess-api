import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_PASSWORD = open("/run/secrets/database_password", "r").read().strip()
DATABASE_HOST = os.environ.get("DATABASE_HOST", "localhost")
DATABASE_PORT = os.environ.get("DATABASE_PORT", 5432)
DATABASE_DB = os.environ.get("DATABASE_DB", "chess")
DATABASE_URL = f"postgresql+psycopg://postgres:{DATABASE_PASSWORD}@{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_DB}"

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)
