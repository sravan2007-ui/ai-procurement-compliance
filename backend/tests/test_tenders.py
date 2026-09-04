from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_create_tender(client):
    payload = {
        "title": "Test Tender",
        "organization": "CPCL",
        "description": "Tender created during automated testing",
        "submission_deadline": "2026-12-31T17:00:00",
    }

    response = client.post(
        "/api/tenders/",
        json=payload,
    )

    assert response.status_code == 200

    data = response.json()

    assert data["title"] == "Test Tender"
    assert data["organization"] == "CPCL"
    assert data["description"] == "Tender created during automated testing"
    assert data["status"] == "DRAFT"


def test_get_tenders(client):
    response = client.get("/api/tenders/")

    assert response.status_code == 200
    assert isinstance(response.json(), list)