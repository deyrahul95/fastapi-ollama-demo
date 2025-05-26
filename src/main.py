from fastapi import FastAPI

from src.routes import ollama_route

app = FastAPI()

app.include_router(ollama_route.router, prefix="/api")

@app.get("/health", tags=["Health"])
def health_check():
    return {
        "status": 200,
        "message": "Api is healthy"
    }