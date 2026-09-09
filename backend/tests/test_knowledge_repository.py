import os

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from app.core.database import Base
from app.models.knowledge_chunk import KnowledgeChunk
from app.models.knowledge_document import KnowledgeDocument
from app.services.rag.knowledge_repository import KnowledgeRepository


DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://sravan@localhost:5432/procurement_db",
)


@pytest.fixture
def db():
    engine = create_engine(DATABASE_URL)

    Base.metadata.create_all(engine)

    with Session(engine) as session:
        yield session

    with Session(engine) as session:
        session.query(KnowledgeChunk).delete()
        session.query(KnowledgeDocument).delete()
        session.commit()

    engine.dispose()


def test_create_document(db):
    repository = KnowledgeRepository(db)

    document = repository.create_document(
        title="GST Guidelines",
        source="Test Source",
        document_type="GST",
        content="GST registration must be valid.",
    )

    db.commit()

    assert document.id is not None
    assert document.title == "GST Guidelines"
    assert document.source == "Test Source"
    assert document.document_type == "GST"


def test_add_chunk(db):
    repository = KnowledgeRepository(db)

    document = repository.create_document(
        title="GST Guidelines",
        source="Test Source",
        document_type="GST",
        content="GST registration must be valid.",
    )

    embedding = [0.0] * 384

    chunk = repository.add_chunk(
        document_id=document.id,
        content="GST registration must be valid.",
        chunk_index=0,
        embedding=embedding,
    )

    db.commit()

    assert chunk.id is not None
    assert chunk.document_id == document.id
    assert len(chunk.embedding) == 384


def test_search_similar(db):
    repository = KnowledgeRepository(db)

    document = repository.create_document(
        title="GST Guidelines",
        source="Test Source",
        document_type="GST",
        content="GST registration must be valid.",
    )

    target_embedding = [0.0] * 384

    repository.add_chunk(
        document_id=document.id,
        content="GST registration must be valid.",
        chunk_index=0,
        embedding=target_embedding,
    )

    repository.add_chunk(
        document_id=document.id,
        content="Unrelated procurement information.",
        chunk_index=1,
        embedding=[1.0] + [0.0] * 383,
    )

    db.commit()

    results = repository.search_similar(
        embedding=target_embedding,
        limit=1,
    )

    assert len(results) == 1
    assert results[0].content == "GST registration must be valid."
