from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel
import httpx
import validators
import time
import re

from app.cache import cache
from app.limiter import limiter

router = APIRouter(prefix="/api", tags=["URL Audit"])


class URLRequest(BaseModel):
    url: str


@router.post("/audit")
@limiter.limit("10/minute")
async def audit(request: Request, body: URLRequest):

    # Validate URL
    if not validators.url(body.url):
        raise HTTPException(status_code=400, detail="Invalid URL")

    # Check cache
    if body.url in cache:
        return {
            "success": True,
            "cached": True,
            **cache[body.url]
        }

    start_time = time.time()

    try:
        async with httpx.AsyncClient(timeout=10) as client:
            response = await client.get(body.url)

        response_time = round((time.time() - start_time) * 1000, 2)

        html = response.text

        title = "No Title Found"

        match = re.search(
            r"<title>(.*?)</title>",
            html,
            re.IGNORECASE | re.DOTALL
        )

        if match:
            title = match.group(1).strip()

        result = {
            "url": body.url,
            "status_code": response.status_code,
            "response_time_ms": response_time,
            "title": title,
            "content_length": len(html)
        }

        cache[body.url] = result

        return {
            "success": True,
            "cached": False,
            **result
        }

    except httpx.TimeoutException:
        raise HTTPException(
            status_code=408,
            detail="Request timed out"
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )