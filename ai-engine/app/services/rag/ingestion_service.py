from dataclasses import dataclass

from app.services.rag.embedding_service import EmbeddingService
from app.services.rag.text_chunker import TextChunker


@dataclass
class IngestedChunk:
    """A chunk ready to be stored in the knowledge base."""

    content: str
    embedding: list[float]
    chunk_index: int


class IngestionService:
    """Prepare knowledge documents for vector storage."""

    def __init__(
        self,
        chunker: TextChunker | None = None,
        embedding_service: EmbeddingService | None = None,
    ) -> None:
        self.chunker = chunker or TextChunker()
        self.embedding_service = (
            embedding_service or EmbeddingService()
        )

    def prepare_chunks(
        self,
        content: str,
    ) -> list[IngestedChunk]:
        """Split content and generate an embedding for each chunk."""
        if not content.strip():
            raise ValueError("Content cannot be empty.")

        chunks = self.chunker.split(content)
        embeddings = self.embedding_service.embed_many(chunks)

        return [
            IngestedChunk(
                content=chunk,
                embedding=embedding,
                chunk_index=index,
            )
            for index, (chunk, embedding) in enumerate(
                zip(chunks, embeddings)
            )
        ]