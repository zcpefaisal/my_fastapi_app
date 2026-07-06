# Application entry point
from fastapi import FastAPI
from app.api.api import api_router
# Importing the rate limit exceeded handler and error class
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
# Importing the rate limiter
from app.core.limiter import limiter


app = FastAPI(title="Enterprice Scalable Async Backend", version="1.0.0")

# Setting up the rate limiter with the FastAPI app
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)


app.include_router(api_router, prefix="/api/v1")

# Root endpoint URL: /
@app.get("/")
def root():
    return {"message": "Welcome to the Enterprice Scalable Async Backend!"}