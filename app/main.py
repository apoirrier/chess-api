import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import app.db.models
from app.api.computer import router as computer_router
from app.api.feedback import router as feedback_router
from app.api.pgn import router as pgn_router
from app.db.base import Base
from app.db.session import engine

app = FastAPI(
    title="Chess Opening Trainer API",
    version="0.1.0",
)

AUTHORIZED_FRONTENDS_ENV = os.environ.get("AUTHORIZED_FRONTENDS", "http://localhost")
AUTHORIZED_FRONTENDS = AUTHORIZED_FRONTENDS_ENV.split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=AUTHORIZED_FRONTENDS,
    allow_methods=["POST", "OPTIONS"],
    allow_headers=["Content-Type", "Accept"],
)

app.include_router(computer_router)
app.include_router(feedback_router)
app.include_router(pgn_router)

Base.metadata.create_all(bind=engine)

@app.get("/")
def root():
    return {"message": "Chess Opening Trainer API."}
