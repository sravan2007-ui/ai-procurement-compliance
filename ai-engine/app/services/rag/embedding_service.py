from sentence_transformers import SentenceTransformer


class EmbeddingService:
    """Generate vector embeddings for RAG text."""

    def __init__(self, model_name: str = "all-MiniLM-L6-v2") -> None:
        self.model = SentenceTransformer(model_name)

    def embed(self, text: str) -> list[float]:
        """Generate a 384-dimensional embedding for one text."""
        if not text.strip():
            raise ValueError("Text cannot be empty.")

        embedding = self.model.encode(
            text,
            normalize_embeddings=True,
        )

        return embedding.tolist()

    def embed_many(self, texts: list[str]) -> list[list[float]]:
        """Generate embeddings for multiple texts."""
        if not texts:
            return []

        if any(not text.strip() for text in texts):
            raise ValueError("Texts cannot contain empty values.")

        embeddings = self.model.encode(
            texts,
            normalize_embeddings=True,
        )

        return embeddings.tolist()