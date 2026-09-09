import pytest
from pydantic import ValidationError

from app.schemas.knowledge import KnowledgeChunkCreate


def test_knowledge_chunk_create():
    chunk = KnowledgeChunkCreate(
        content="GST registration must be valid.",
        chunk_index=0,
        embedding=[0.0] * 384,
    )

    assert chunk.content == "GST registration must be valid."
    assert chunk.chunk_index == 0
    assert len(chunk.embedding) == 384


def test_knowledge_chunk_rejects_invalid_index():
    with pytest.raises(ValidationError):
        KnowledgeChunkCreate(
            content="GST registration must be valid.",
            chunk_index=-1,
            embedding=[0.0] * 384,
        )


def test_knowledge_chunk_rejects_wrong_embedding_size():
    with pytest.raises(ValidationError):
        KnowledgeChunkCreate(
            content="GST registration must be valid.",
            chunk_index=0,
            embedding=[0.0] * 383,
        )


def test_knowledge_chunk_rejects_empty_content():
    with pytest.raises(ValidationError):
        KnowledgeChunkCreate(
            content="",
            chunk_index=0,
            embedding=[0.0] * 384,
        )
