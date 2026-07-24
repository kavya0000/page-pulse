import uuid
import logging

from fastapi import FastAPI, Request
from app.api import router


logging.basicConfig(level=logging.INFO)

logger = logging.getLogger("page-pulse")


app = FastAPI(
    title="Page Pulse API"
)


@app.middleware("http")
async def add_request_id(request: Request, call_next):

    request_id = str(uuid.uuid4())

    logger.info(
        f"Request started | ID={request_id}"
    )

    response = await call_next(request)

    response.headers["X-Request-ID"] = request_id

    logger.info(
        f"Request completed | ID={request_id}"
    )

    return response



app.include_router(router)


@app.get("/")
def home():

    return {
        "message": "Page Pulse API",
        "status": "running",
        "credit": "Built for Digital Heroes Training Task - https://digitalheroesco.com"
    }