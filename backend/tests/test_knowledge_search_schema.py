import pytest
from pydantic import ValidationError

from app.schemas.knowledge import (
    KnowledgeSearchRequest,
    KnowledgeSearchResult,
)


def test_knowledge_search_request():
    request = KnowledgeSearchRequest(
        embedding=[0.0] * 384,
        limit=5,
    )

    assert len(request.embedding) == 384
    assert request.limit == 5


def test_search_request_rejects_wrong_embedding_size():
    with pytest.raises(ValidationError):
        KnowledgeSearchRequest(
            embedding=[0.0] * 383,
        )


def test_search_request_rejects_invalid_limit():
    with pytest.raises(ValidationError):
        KnowledgeSearchRequest(
            embedding=[0.0] * 384,
            limit=0,
        )


def test_knowledge_search_result():
    result = KnowledgeSearchResult(
        id=1,
        document_id=10,
        content="GST registration must be valid.",
        chunk_index=0,
    )

    assert result.id == 1
    assert result.document_id == 10
    assert result.content == "GST registration must be valid."
    assert result.chunk_index == 0
