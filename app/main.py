from fastapi import FastAPI

from app.api.computer import router as computer_router
from app.api.feedback import router as feedback_router

app = FastAPI(
    title="Chess Opening Trainer API",
    version="0.1.0",
)

app.include_router(computer_router)
app.include_router(feedback_router)


@app.get("/")
def root():
    return {"message": "Chess Opening Trainer API"}