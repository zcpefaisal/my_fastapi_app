# Application entry point
from fastapi import FastAPI

app = FastAPI(title="Enterprice Scalable Async Backend", version="1.0.0")

@app.get("/")
def root():
    return {"message": "Welcome to the Enterprice Scalable Async Backend!"}