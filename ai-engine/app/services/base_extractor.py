from abc import ABC, abstractmethod
from typing import TypeVar

from pydantic import BaseModel

from app.services.document_extractor import DocumentExtractor
from app.services.gemini_client import GeminiClient


T = TypeVar("T", bound=BaseModel)


class BaseDocumentExtractor(ABC):
    """Base class for AI-powered document extraction."""

    def __init__(
        self,
        document_extractor: DocumentExtractor | None = None,
        gemini_client: GeminiClient | None = None,
    ) -> None:
        self.document_extractor = (
            document_extractor or DocumentExtractor()
        )
        self.gemini_client = gemini_client or GeminiClient()

    @property
    @abstractmethod
    def response_model(self) -> type[T]:
        """Return the Pydantic model for the document."""
        raise NotImplementedError

    @abstractmethod
    def build_prompt(self, text: str) -> str:
        """Build the document-specific extraction prompt."""
        raise NotImplementedError

    def extract(self, file_path: str) -> T:
        """Extract structured information from a document."""

        text = self.document_extractor.extract_text(file_path)

        if not text:
            raise ValueError(
                "No text could be extracted from the document."
            )

        prompt = self.build_prompt(text)

        return self.gemini_client.generate_structured(
            prompt=prompt,
            response_model=self.response_model,
        )