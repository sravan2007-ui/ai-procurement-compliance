from io import BytesIO
import pymupdf
from unittest.mock import patch

def create_test_bid(client):
    """Create a tender, bidder, and bid for document tests."""

    tender_payload = {
        "title": "Document Test Tender",
        "organization": "CPCL",
        "description": "Tender for document API testing",
        "submission_deadline": "2026-12-31T17:00:00",
    }

    tender_response = client.post(
        "/api/tenders/",
        json=tender_payload,
    )

    assert tender_response.status_code == 200

    tender = tender_response.json()

    bidder_payload = {
        "company_name": "Document Test Company Pvt Ltd",
        "pan": "DOCTP1234A",
        "gstin": "33DOCTP1234A1Z5",
        "udyam_number": "UDYAM-TN-DOC-001",
        "cin": "U45200TN2026PTC777777",
        "email": "documenttest@example.com",
        "phone": "9876511111",
    }

    bidder_response = client.post(
        "/api/bidders/",
        json=bidder_payload,
    )

    assert bidder_response.status_code == 200

    bidder = bidder_response.json()

    bid_response = client.post(
        "/api/bids/",
        json={
            "tender_id": tender["id"],
            "bidder_id": bidder["id"],
        },
    )

    assert bid_response.status_code == 200

    return bid_response.json()["id"]


def test_upload_pdf_document(client):
    bid_id = create_test_bid(client)

    pdf_content = b"%PDF-1.4\nTest PDF content"

    response = client.post(
        "/api/documents/",
        data={
            "bid_id": str(bid_id),
            "document_type": "GST_CERTIFICATE",
        },
        files={
            "file": (
                "test_gst.pdf",
                BytesIO(pdf_content),
                "application/pdf",
            )
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["bid_id"] == bid_id
    assert data["document_type"] == "GST_CERTIFICATE"
    assert data["file_name"] == "test_gst.pdf"
    assert data["mime_type"] == "application/pdf"
    assert data["status"] == "UPLOADED"


def test_upload_rejects_unsupported_file_type(client):
    bid_id = create_test_bid(client)

    response = client.post(
        "/api/documents/",
        data={
            "bid_id": str(bid_id),
            "document_type": "GST_CERTIFICATE",
        },
        files={
            "file": (
                "test.txt",
                BytesIO(b"This is not a supported document"),
                "text/plain",
            )
        },
    )

    assert response.status_code == 400

    assert response.json()["detail"] == (
        "Unsupported file type. "
        "Only PDF, JPEG, and PNG are allowed."
    )


def test_upload_document_with_invalid_bid(client):
    response = client.post(
        "/api/documents/",
        data={
            "bid_id": "999999",
            "document_type": "GST_CERTIFICATE",
        },
        files={
            "file": (
                "test.pdf",
                BytesIO(b"%PDF-1.4"),
                "application/pdf",
            )
        },
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Bid not found"


def create_test_pdf():
    document = pymupdf.open()

    page = document.new_page()

    page.insert_text(
        (72, 72),
        "GST Certificate\n"
        "GSTIN: 33DOCTP1234A1Z5\n"
        "Legal Name: Document Test Company Pvt Ltd\n"
        "Status: Active",
    )

    pdf_bytes = document.tobytes()

    document.close()

    return pdf_bytes

def test_process_image_returns_422(client):
    bid_id = create_test_bid(client)

    response = client.post(
        "/api/documents/",
        data={
            "bid_id": str(bid_id),
            "document_type": "GST_CERTIFICATE",
        },
        files={
            "file": (
                "test_image.png",
                b"fake image content",
                "image/png",
            )
        },
    )

    assert response.status_code == 200

    document = response.json()

    process_response = client.post(
        f"/api/documents/{document['id']}/process"
    )

    assert process_response.status_code == 422

    assert process_response.json()["detail"] == (
        "OCR processing is not available yet. "
        "Only PDF documents with extractable text "
        "are currently supported."
    )

def test_process_pdf_successfully(client):
    bid_id = create_test_bid(client)

    pdf_content = create_test_pdf()

    upload_response = client.post(
        "/api/documents/",
        data={
            "bid_id": str(bid_id),
            "document_type": "GST_CERTIFICATE",
        },
        files={
            "file": (
                "test_gst.pdf",
                pdf_content,
                "application/pdf",
            )
        },
    )

    assert upload_response.status_code == 200

    document = upload_response.json()

    fake_extracted_data = {
        "gstin": "33DOCTP1234A1Z5",
        "legal_name": "Document Test Company Pvt Ltd",
        "trade_name": "Document Test Company",
        "registration_date": "15/04/2022",
        "business_type": "Private Limited Company",
        "status": "Active",
        "principal_place_of_business": "Chennai, Tamil Nadu",
    }

    with patch(
        "app.api.documents.AIExtractor"
    ) as mock_extractor:

        mock_instance = mock_extractor.return_value

        mock_instance.extract.return_value = (
            type(
                "FakeExtraction",
                (),
                {
                    "model_dump": lambda self: fake_extracted_data
                },
            )()
        )

        process_response = client.post(
            f"/api/documents/{document['id']}/process"
        )

    assert process_response.status_code == 200

    data = process_response.json()

    assert data["document_id"] == document["id"]
    assert data["status"] == "PROCESSED"

    assert data["extracted_data"]["gstin"] == (
        "33DOCTP1234A1Z5"
    )

    assert data["extracted_data"]["legal_name"] == (
        "Document Test Company Pvt Ltd"
    )

def test_get_latest_extraction(client):
    bid_id = create_test_bid(client)

    pdf_content = create_test_pdf()

    upload_response = client.post(
        "/api/documents/",
        data={
            "bid_id": str(bid_id),
            "document_type": "GST_CERTIFICATE",
        },
        files={
            "file": (
                "test_gst.pdf",
                pdf_content,
                "application/pdf",
            )
        },
    )

    assert upload_response.status_code == 200

    document_id = upload_response.json()["id"]

    fake_extracted_data = {
        "gstin": "33DOCTP1234A1Z5",
        "legal_name": "Document Test Company Pvt Ltd",
        "trade_name": "Document Test Company",
        "registration_date": "15/04/2022",
        "business_type": "Private Limited Company",
        "status": "Active",
        "principal_place_of_business": "Chennai, Tamil Nadu",
    }

    with patch(
        "app.api.documents.AIExtractor"
    ) as mock_extractor:

        mock_instance = mock_extractor.return_value

        mock_instance.extract.return_value = (
            type(
                "FakeExtraction",
                (),
                {
                    "model_dump": lambda self: fake_extracted_data
                },
            )()
        )

        process_response = client.post(
            f"/api/documents/{document_id}/process"
        )

    assert process_response.status_code == 200

    response = client.get(
        f"/api/documents/{document_id}/extractions/latest"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["document_id"] == document_id
    assert data["document_type"] == "GST_CERTIFICATE"
    assert data["extraction_status"] == "COMPLETED"
    assert data["model_name"] == "gemini-2.5-flash"
    assert data["extracted_data"]["gstin"] == "33DOCTP1234A1Z5"

def test_get_extraction_history(client):
    bid_id = create_test_bid(client)

    pdf_content = create_test_pdf()

    upload_response = client.post(
        "/api/documents/",
        data={
            "bid_id": str(bid_id),
            "document_type": "GST_CERTIFICATE",
        },
        files={
            "file": (
                "test_gst.pdf",
                pdf_content,
                "application/pdf",
            )
        },
    )

    assert upload_response.status_code == 200

    document_id = upload_response.json()["id"]

    fake_extracted_data = {
        "gstin": "33DOCTP1234A1Z5",
        "legal_name": "Document Test Company Pvt Ltd",
        "trade_name": "Document Test Company",
        "registration_date": "15/04/2022",
        "business_type": "Private Limited Company",
        "status": "Active",
        "principal_place_of_business": "Chennai, Tamil Nadu",
    }

    with patch(
        "app.api.documents.AIExtractor"
    ) as mock_extractor:

        mock_instance = mock_extractor.return_value

        mock_instance.extract.return_value = (
            type(
                "FakeExtraction",
                (),
                {
                    "model_dump": lambda self: fake_extracted_data
                },
            )()
        )

        client.post(
            f"/api/documents/{document_id}/process"
        )

        client.post(
            f"/api/documents/{document_id}/process"
        )

    response = client.get(
        f"/api/documents/{document_id}/extractions"
    )

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 2

    # Newest extraction should appear first.
    assert data[0]["id"] > data[1]["id"]

    assert data[0]["document_id"] == document_id
    assert data[1]["document_id"] == document_id