from fastapi import FastAPI

app = FastAPI(
    title="Perpetua API",
    description="API for the AI-powered language learning platform.",
    version="0.1.0"
)

@app.get("/")
def read_root():
    """
    Root endpoint to check if the API is running.
    """
    return {"message": "Welcome to the Perpetua API!"}