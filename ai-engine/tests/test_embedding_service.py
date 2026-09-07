from app.services.rag.embedding_service import EmbeddingService


def test_embed_returns_384_dimensions():
    service = EmbeddingService()

    embedding = service.embed("GST registration must be valid.")

    assert len(embedding) == 384
    assert all(isinstance(value, float) for value in embedding)


def test_embed_rejects_empty_text():
    service = EmbeddingService()

    try:
        service.embed("   ")
        assert False, "Expected ValueError"
    except ValueError as exc:
        assert str(exc) == "Text cannot be empty."


def test_embed_many_returns_embeddings():
    service = EmbeddingService()

    embeddings = service.embed_many(
        [
            "GST registration must be valid.",
            "Bidder must submit PAN.",
        ]
    )

    assert len(embeddings) == 2
    assert all(len(embedding) == 384 for embedding in embeddings)


def test_embed_many_rejects_empty_values():
    service = EmbeddingService()

    try:
        service.embed_many(
            [
                "GST registration must be valid.",
                "   ",
            ]
        )
        assert False, "Expected ValueError"
    except ValueError as exc:
        assert str(exc) == "Texts cannot contain empty values."