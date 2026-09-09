def test_create_knowledge_chunk(client):
    document_response = client.post(
        "/api/knowledge/documents",
        json={
            "title": "GST Guidelines",
            "source": "Government Portal",
            "document_type": "GST",
            "content": "GST registration must be valid.",
        },
    )

    assert document_response.status_code == 201

    document_id = document_response.json()["id"]

    response = client.post(
        f"/api/knowledge/documents/{document_id}/chunks",
        json={
            "content": "GST registration must be valid.",
            "chunk_index": 0,
            "embedding": [0.0] * 384,
        },
    )

    assert response.status_code == 201
    assert response.json()["id"] > 0


def test_create_knowledge_chunk_rejects_invalid_embedding(client):
    document_response = client.post(
        "/api/knowledge/documents",
        json={
            "title": "GST Guidelines",
            "source": "Government Portal",
            "document_type": "GST",
            "content": "GST registration must be valid.",
        },
    )

    document_id = document_response.json()["id"]

    response = client.post(
        f"/api/knowledge/documents/{document_id}/chunks",
        json={
            "content": "GST registration must be valid.",
            "chunk_index": 0,
            "embedding": [0.0] * 383,
        },
    )

    assert response.status_code == 422
