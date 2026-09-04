def test_create_bidder(client):
    payload = {
        "company_name": "Test Construction Pvt Ltd",
        "pan": "TESTP1234A",
        "gstin": "33TESTP1234A1Z5",
        "udyam_number": "UDYAM-TN-TEST-001",
        "cin": "U45200TN2026PTC123456",
        "email": "test@example.com",
        "phone": "9876543210",
    }

    response = client.post(
        "/api/bidders/",
        json=payload,
    )

    assert response.status_code == 200

    data = response.json()

    assert data["company_name"] == "Test Construction Pvt Ltd"
    assert data["pan"] == "TESTP1234A"
    assert data["gstin"] == "33TESTP1234A1Z5"
    assert data["email"] == "test@example.com"


def test_get_bidders(client):
    response = client.get("/api/bidders/")

    assert response.status_code == 200
    assert isinstance(response.json(), list)