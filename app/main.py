from fastapi import FastAPI

from app.api.moves import router as moves_router
from app.api.feedback import router as feedback_router

app = FastAPI(
    title="Chess Opening Trainer API",
    version="0.1.0",
)

app.include_router(moves_router)
app.include_router(feedback_router)


@app.get("/")
def root():
    return {"message": "Chess Opening Trainer API"}