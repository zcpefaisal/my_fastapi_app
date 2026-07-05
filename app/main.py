# Application entry point
from fastapi import FastAPI
from app.api.api import api_router

app = FastAPI(title="Enterprice Scalable Async Backend", version="1.0.0")

app.include_router(api_router, prefix="/api/v1")

# Root endpoint URL: /
@app.get("/")
def root():
    return {"message": "Welcome to the Enterprice Scalable Async Backend!"}