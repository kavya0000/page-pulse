from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_home():
    response = client.get("/")

    assert response.status_code == 200

    data = response.json()

    assert data["message"] == "Page Pulse API"
    assert data["status"] == "running"
    assert "Digital Heroes Training Task" in data["credit"]


def test_invalid_url():

    response = client.post(
        "/api/audit",
        json={
            "url": "invalid-url"
        }
    )

    assert response.status_code == 400


def test_google_audit():

    response = client.post(
        "/api/audit",
        json={
            "url": "https://www.google.com"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["success"] is True
    assert data["status_code"] == 200