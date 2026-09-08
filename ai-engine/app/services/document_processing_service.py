from typing import Any

from app.models.document_type import DocumentType, DocumentTypeResult
from app.services.document_type_detector import DocumentTypeDetector
from app.services.financial_extractor import FinancialExtractor
from app.services.experience_extractor import ExperienceExtractor
from app.services.gst_extractor import GSTExtractor
from app.services.pan_extractor import PANExtractor
from app.services.udyam_extractor import UdyamExtractor


class DocumentProcessingService:
    """Classify a bidder document and extract structured information."""

    def __init__(
        self,
        document_type_detector: DocumentTypeDetector | None = None,
        extractors: dict[DocumentType, Any] | None = None,
    ) -> None:
        self.document_type_detector = (
            document_type_detector or DocumentTypeDetector()
        )

        self.extractors = extractors or {
            DocumentType.GST_CERTIFICATE: GSTExtractor(),
            DocumentType.UDYAM_CERTIFICATE: UdyamExtractor(),
            DocumentType.PAN: PANExtractor(),
            DocumentType.FINANCIAL_STATEMENT: FinancialExtractor(),
            DocumentType.EXPERIENCE_CERTIFICATE: ExperienceExtractor(),
        }

    def process(self, file_path: str) -> tuple[DocumentTypeResult, Any | None]:
        """Classify the document and extract structured information."""

        classification = self.document_type_detector.detect(file_path)

        if classification.document_type == DocumentType.OTHER:
            return classification, None

        extractor = self.extractors.get(classification.document_type)

        if extractor is None:
            raise ValueError(
                f"No extractor configured for document type: "
                f"{classification.document_type}"
            )

        extracted_data = extractor.extract(file_path)

        return classification, extracted_data