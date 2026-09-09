from app.models.knowledge_chunk import KnowledgeChunk
from app.models.knowledge_document import KnowledgeDocument


def test_knowledge_search_returns_similar_chunks(client, db_session):
    document = KnowledgeDocument(
        title="GST Compliance Rules",
        source="Test Source",
        document_type="procurement_rule",
        content="GST registration must be valid.",
    )

    db_session.add(document)
    db_session.flush()

    chunk = KnowledgeChunk(
        document_id=document.id,
        content="GST registration must be valid.",
        chunk_index=0,
        embedding=[1.0] + [0.0] * 383,
    )

    db_session.add(chunk)
    db_session.commit()

    response = client.post(
        "/api/knowledge/search",
        json={
            "embedding": [1.0] + [0.0] * 383,
            "limit": 5,
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert len(data) >= 1

    matching_results = [
        result for result in data
        if result["id"] == chunk.id
    ]

    assert len(matching_results) == 1

    result = matching_results[0]

    assert result["document_id"] == document.id
    assert result["content"] == "GST registration must be valid."
    assert result["chunk_index"] == 0
