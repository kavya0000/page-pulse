# Page Pulse API

A production-ready URL Audit API built with FastAPI.

## Live Deployment 🚀

Production API:
https://page-pulse-oci2.onrender.com

Swagger API Documentation:
https://page-pulse-oci2.onrender.com/docs

API Status:
✅ Production Ready

## Features

- URL Validation
- Website Status Check
- Response Time Measurement
- HTML Title Extraction
- URL Response Caching
- Rate Limiting
- Swagger API Documentation
- Automated Tests using Pytest
- GitHub Actions CI

## Installation

```bash
pip install -r requirements.txt
```

## Run the Application

```bash
uvicorn app.main:app --reload
```

The API will be available at:

```
http://127.0.0.1:8000
```

## API Documentation

Swagger UI:

```
http://127.0.0.1:8000/docs
```

## Example Request

```json
{
  "url": "https://www.google.com"
}
```

## Example Response

```json
{
  "success": true,
  "cached": false,
  "url": "https://www.google.com",
  "status_code": 200,
  "response_time_ms": 871.78,
  "title": "Google",
  "content_length": 80684
}


## Run Tests

```bash
python -m pytest
```

## Project Structure

```
page-pulse/
│── app/
│   ├── api.py
│   ├── cache.py
│   ├── limiter.py
│   ├── main.py
│   └── __init__.py
│
│── tests/
│   └── test_api.py
│
│── .github/
│   └── workflows/
│       └── ci.yml
│
│── requirements.txt
│── README.md
│── .gitignore
```


## Tech Stack

- Python
- FastAPI
- HTTPX
- CacheTools
- SlowAPI
- Pytest
- GitHub Actions
- Render Cloud Deployment

## Author

**Kavya Poleboina**
