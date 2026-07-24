from fastapi import FastAPI
from slowapi.middleware import SlowAPIMiddleware
from app.api import router
from app.limiter import limiter

app = FastAPI(
    title="Page Pulse API",
    description="Production URL Audit Service",
    version="1.0.0"
)

app.state.limiter = limiter
app.add_middleware(SlowAPIMiddleware)

app.include_router(router)

@app.get("/")
async def home():
    return {
        "message": "Page Pulse API Running Successfully",
        "version": "1.0.0"
    }