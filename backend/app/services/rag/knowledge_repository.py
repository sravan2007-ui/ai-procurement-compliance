from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.knowledge_chunk import KnowledgeChunk
from app.models.knowledge_document import KnowledgeDocument


class KnowledgeRepository:
    """Store and retrieve knowledge documents and vector chunks."""

    def __init__(self, db: Session) -> None:
        self.db = db

    def create_document(
        self,
        title: str,
        source: str,
        document_type: str,
        content: str,
    ) -> KnowledgeDocument:
        document = KnowledgeDocument(
            title=title,
            source=source,
            document_type=document_type,
            content=content,
        )

        self.db.add(document)
        self.db.flush()

        return document

    def add_chunk(
        self,
        document_id: int,
        content: str,
        chunk_index: int,
        embedding: list[float],
    ) -> KnowledgeChunk:
        chunk = KnowledgeChunk(
            document_id=document_id,
            content=content,
            chunk_index=chunk_index,
            embedding=embedding,
        )

        self.db.add(chunk)
        self.db.flush()

        return chunk

    def search_similar(
        self,
        embedding: list[float],
        limit: int = 5,
    ) -> list[KnowledgeChunk]:
        statement = (
            select(KnowledgeChunk)
            .order_by(KnowledgeChunk.embedding.cosine_distance(embedding))
            .limit(limit)
        )

        return list(self.db.scalars(statement).all())
