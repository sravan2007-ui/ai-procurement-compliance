def test_create_bid(client):
    # Create a tender first
    tender_payload = {
        "title": "Bid Test Tender",
        "organization": "CPCL",
        "description": "Tender for bid API testing",
        "submission_deadline": "2026-12-31T17:00:00",
    }

    tender_response = client.post(
        "/api/tenders/",
        json=tender_payload,
    )

    assert tender_response.status_code == 200

    tender = tender_response.json()

    # Create a bidder
    bidder_payload = {
        "company_name": "Bid Test Company Pvt Ltd",
        "pan": "BIDTP1234A",
        "gstin": "33BIDTP1234A1Z5",
        "udyam_number": "UDYAM-TN-BID-001",
        "cin": "U45200TN2026PTC654321",
        "email": "bidtest@example.com",
        "phone": "9876501234",
    }

    bidder_response = client.post(
        "/api/bidders/",
        json=bidder_payload,
    )

    assert bidder_response.status_code == 200

    bidder = bidder_response.json()

    # Create the bid
    bid_payload = {
        "tender_id": tender["id"],
        "bidder_id": bidder["id"],
    }

    response = client.post(
        "/api/bids/",
        json=bid_payload,
    )

    assert response.status_code == 200

    data = response.json()

    assert data["tender_id"] == tender["id"]
    assert data["bidder_id"] == bidder["id"]
    assert data["status"] == "SUBMITTED"


def test_create_bid_with_invalid_tender(client):
    # Create a bidder
    bidder_payload = {
        "company_name": "Invalid Tender Test Company",
        "pan": "INVAL1234A",
        "gstin": "33INVAL1234A1Z5",
        "udyam_number": "UDYAM-TN-INVALID-001",
        "cin": "U45200TN2026PTC111111",
        "email": "invalid@example.com",
        "phone": "9876512345",
    }

    bidder_response = client.post(
        "/api/bidders/",
        json=bidder_payload,
    )

    assert bidder_response.status_code == 200

    bidder = bidder_response.json()

    bid_payload = {
        "tender_id": 999999,
        "bidder_id": bidder["id"],
    }

    response = client.post(
        "/api/bids/",
        json=bid_payload,
    )

    assert response.status_code == 404