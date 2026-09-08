class TextChunker:
    """Split long text into overlapping chunks for RAG."""

    def __init__(
        self,
        chunk_size: int = 500,
        chunk_overlap: int = 50,
    ) -> None:
        if chunk_size <= 0:
            raise ValueError("Chunk size must be greater than 0.")

        if chunk_overlap < 0:
            raise ValueError("Chunk overlap cannot be negative.")

        if chunk_overlap >= chunk_size:
            raise ValueError(
                "Chunk overlap must be smaller than chunk size."
            )

        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    def split(self, text: str) -> list[str]:
        """Split text into overlapping chunks."""
        if not text.strip():
            raise ValueError("Text cannot be empty.")

        text = text.strip()

        if len(text) <= self.chunk_size:
            return [text]

        chunks: list[str] = []
        start = 0
        step = self.chunk_size - self.chunk_overlap

        while start < len(text):
            end = start + self.chunk_size
            chunk = text[start:end].strip()

            if chunk:
                chunks.append(chunk)

            start += step

        return chunks