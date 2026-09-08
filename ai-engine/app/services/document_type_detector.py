from app.models.document_type import DocumentType, DocumentTypeResult
from app.services.base_extractor import BaseDocumentExtractor


class DocumentTypeDetector:
    """Classify an uploaded document into a supported document type."""

    def __init__(
        self,
        document_extractor=None,
        gemini_client=None,
    ) -> None:
        self.document_extractor = document_extractor
        self.gemini_client = gemini_client

        if self.document_extractor is None:
            from app.services.document_extractor import DocumentExtractor

            self.document_extractor = DocumentExtractor()

        if self.gemini_client is None:
            from app.services.gemini_client import GeminiClient

            self.gemini_client = GeminiClient()

    def detect(self, file_path: str) -> DocumentTypeResult:
        """Detect the type of an uploaded document."""

        text = self.document_extractor.extract_text(file_path)

        if not text:
            raise ValueError(
                "No text could be extracted from the document."
            )

        prompt = f"""
You are a government procurement document classification assistant.

Classify the following document into exactly one of these types:

- GST_CERTIFICATE
- UDYAM_CERTIFICATE
- PAN
- FINANCIAL_STATEMENT
- EXPERIENCE_CERTIFICATE
- OTHER

Rules:
- Choose OTHER if the document does not clearly match a supported type.
- Do not invent information.
- Return a confidence score between 0 and 1.
- Give a short reason for your classification.

DOCUMENT TEXT:
{text}
"""

        return self.gemini_client.generate_structured(
            prompt=prompt,
            response_model=DocumentTypeResult,
        )