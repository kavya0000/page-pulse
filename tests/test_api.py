from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_home():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["message"] == "Page Pulse API Running Successfully"


def test_invalid_url():
    response = client.post(
        "/api/audit",
        json={"url": "invalid-url"}
    )

    assert response.status_code == 400


def test_valid_url():
    response = client.post(
        "/api/audit",
        json={"url": "https://www.google.com"}
    )

    assert response.status_code == 200
    assert "status_code" in response.json()