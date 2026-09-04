from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_root(client):
    response = client.get("/")

    assert response.status_code == 200
    assert response.json()["message"] == "AI Procurement Compliance Platform"


def test_health(client):
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "healthy"