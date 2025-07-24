from fastapi import FastAPI

from app.api.v1.api import api_router
from app.db.models import user
from app.db.base import Base, engine

Base.metadata.create_all(bind=engine)
app = FastAPI(
    title="Perpetua API",
    description="API for the AI-powered language learning platform.",
    version="0.1.0"
)

app.include_router(api_router, prefix="/api/v1")

@app.get("/")
def read_root():
    """
    Root endpoint to check if the API is running.
    """
    return {"message": "Welcome to the Perpetua API!"}