from app.services.rag.ingestion_service import IngestionService


class FakeEmbeddingService:
    def embed_many(self, texts: list[str]) -> list[list[float]]:
        return [[float(index)] * 384 for index, _ in enumerate(texts)]


class FakeChunker:
    def split(self, text: str) -> list[str]:
        return [
            "GST registration must be valid.",
            "PAN must be submitted.",
        ]


def test_prepare_chunks_creates_embeddings():
    service = IngestionService(
        chunker=FakeChunker(),
        embedding_service=FakeEmbeddingService(),
    )

    chunks = service.prepare_chunks(
        "GST registration must be valid. PAN must be submitted."
    )

    assert len(chunks) == 2

    assert chunks[0].content == "GST registration must be valid."
    assert chunks[0].chunk_index == 0
    assert len(chunks[0].embedding) == 384

    assert chunks[1].content == "PAN must be submitted."
    assert chunks[1].chunk_index == 1
    assert len(chunks[1].embedding) == 384


def test_prepare_chunks_rejects_empty_content():
    service = IngestionService(
        chunker=FakeChunker(),
        embedding_service=FakeEmbeddingService(),
    )

    try:
        service.prepare_chunks("   ")
        assert False, "Expected ValueError"
    except ValueError as exc:
        assert str(exc) == "Content cannot be empty."