import pytest
from pydantic import ValidationError

from app.schemas.knowledge import (
    KnowledgeDocumentCreate,
    KnowledgeDocumentResponse,
)


def test_knowledge_document_create():
    document = KnowledgeDocumentCreate(
        title="GST Guidelines",
        source="Government Portal",
        document_type="GST",
        content="GST registration must be valid.",
    )

    assert document.title == "GST Guidelines"
    assert document.source == "Government Portal"
    assert document.document_type == "GST"
    assert document.content == "GST registration must be valid."


def test_knowledge_document_requires_content():
    with pytest.raises(ValidationError):
        KnowledgeDocumentCreate(
            title="GST Guidelines",
            source="Government Portal",
            document_type="GST",
            content="",
        )


def test_knowledge_document_response():
    document = KnowledgeDocumentResponse(
        id=1,
        title="GST Guidelines",
        source="Government Portal",
        document_type="GST",
    )

    assert document.id == 1
    assert document.title == "GST Guidelines"
