from typing import Any

import requests

from app.core.config import settings


class RAGClientError(RuntimeError):
    """Raised when the backend RAG service cannot be reached."""


class RAGClient:
    def __init__(
        self,
        base_url: str | None = None,
    ) -> None:
        self.base_url = (
            base_url or settings.backend_url
        ).rstrip("/")

    def search(
        self,
        embedding: list[float],
        limit: int = 5,
    ) -> list[dict[str, Any]]:
        try:
            response = requests.post(
                f"{self.base_url}/api/knowledge/search",
                json={
                    "embedding": embedding,
                    "limit": limit,
                },
                timeout=10,
            )
            response.raise_for_status()
        except requests.RequestException as exc:
            raise RAGClientError(
                "RAG backend service is currently unavailable."
            ) from exc

        return response.json()
