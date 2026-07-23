from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import app.db.models
from app.api.computer import router as computer_router
from app.api.feedback import router as feedback_router
from app.db.base import Base
from app.db.session import engine

app = FastAPI(
    title="Chess Opening Trainer API",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["POST", "OPTIONS"],
    allow_headers=["Content-Type", "Accept"],
)

app.include_router(computer_router)
app.include_router(feedback_router)

Base.metadata.create_all(bind=engine)

@app.get("/")
def root():
    return {"message": "Chess Opening Trainer API."}
