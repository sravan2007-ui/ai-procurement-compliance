from app.services.rag.rag_service import RAGService


class FakeEmbeddingService:
    def embed(self, text):
        assert text == "GST compliance requirement"
        return [0.1] * 384


class FakeRAGClient:
    def search(self, embedding, limit):
        assert len(embedding) == 384
        assert limit == 3

        return [
            {
                "id": 17,
                "document_id": 18,
                "content": "A bidder must have a valid GST registration.",
                "chunk_index": 0,
            }
        ]


def test_rag_service_retrieve():
    service = RAGService(
        embedding_service=FakeEmbeddingService(),
        rag_client=FakeRAGClient(),
    )

    results = service.retrieve(
        query="GST compliance requirement",
        limit=3,
    )

    assert len(results) == 1
    assert results[0]["id"] == 17
    assert results[0]["document_id"] == 18
    assert results[0]["content"] == (
        "A bidder must have a valid GST registration."
    )


def test_rag_service_rejects_empty_query():
    service = RAGService(
        embedding_service=FakeEmbeddingService(),
        rag_client=FakeRAGClient(),
    )

    try:
        service.retrieve("")
        assert False, "Expected ValueError"
    except ValueError as exc:
        assert str(exc) == "Query cannot be empty."
