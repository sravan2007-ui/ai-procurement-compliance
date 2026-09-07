from typing import Any

from app.services.rag.embedding_service import EmbeddingService
from app.services.rag.rag_client import RAGClient


class RAGService:
    def __init__(
        self,
        embedding_service: EmbeddingService | None = None,
        rag_client: RAGClient | None = None,
    ) -> None:
        self.embedding_service = (
            embedding_service or EmbeddingService()
        )
        self.rag_client = rag_client or RAGClient()

    def retrieve(
        self,
        query: str,
        limit: int = 5,
    ) -> list[dict[str, Any]]:
        if not query.strip():
            raise ValueError("Query cannot be empty.")

        embedding = self.embedding_service.embed(query)

        return self.rag_client.search(
            embedding=embedding,
            limit=limit,
        )
