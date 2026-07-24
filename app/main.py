from fastapi import FastAPI, Request
import uuid
import logging

from app.api import router

app = FastAPI(
    title="Page Pulse API",
    version="1.0.0",
    description="Production URL Audit Service"
)


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s"
)

logger = logging.getLogger("page-pulse")


@app.middleware("http")
async def request_id_middleware(request: Request, call_next):

    request_id = str(uuid.uuid4())

    logger.info(
        f"request_started request_id={request_id} path={request.url.path}"
    )

    response = await call_next(request)

    response.headers["X-Request-ID"] = request_id

    logger.info(
        f"request_completed request_id={request_id} status={response.status_code}"
    )

    return response


@app.get("/")
def home():

    return {
        "message": "Page Pulse API",
        "status": "running",
        "credit": "Built for Digital Heroes Training Task - https://digitalheroesco.com"
    }


app.include_router(router)