def test_create_knowledge_document(client):
    response = client.post(
        "/api/knowledge/documents",
        json={
            "title": "GST Guidelines",
            "source": "Government Portal",
            "document_type": "GST",
            "content": "GST registration must be valid.",
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert data["id"] > 0
    assert data["title"] == "GST Guidelines"
    assert data["source"] == "Government Portal"
    assert data["document_type"] == "GST"


def test_create_knowledge_document_rejects_empty_content(client):
    response = client.post(
        "/api/knowledge/documents",
        json={
            "title": "GST Guidelines",
            "source": "Government Portal",
            "document_type": "GST",
            "content": "",
        },
    )

    assert response.status_code == 422
