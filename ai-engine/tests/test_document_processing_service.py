import pymupdf

from app.models.document_type import DocumentType, DocumentTypeResult
from app.models.pan import PANDocument
from app.services.document_processing_service import DocumentProcessingService


class FakeDocumentTypeDetector:
    """Fake classifier used for unit testing."""

    def __init__(self, result):
        self.result = result

    def detect(self, file_path):
        return self.result


class FakePANExtractor:
    """Fake PAN extractor used for unit testing."""

    def extract(self, file_path):
        return PANDocument(
            pan_number="ABCDE1234F",
            holder_name="ABC Technologies Pvt Ltd",
            document_type="PAN Card",
            raw_text="sample PAN document",
            confidence=0.97,
            warnings=[],
        )


def create_pdf(path):
    document = pymupdf.open()
    page = document.new_page()
    page.insert_text(
        (72, 72),
        "Permanent Account Number Card\n"
        "ABC Technologies Pvt Ltd\n"
        "ABCDE1234F",
    )
    document.save(path)
    document.close()


def test_document_processing_service_routes_to_correct_extractor(tmp_path):
    pdf_path = tmp_path / "pan.pdf"
    create_pdf(pdf_path)

    classification = DocumentTypeResult(
        document_type=DocumentType.PAN,
        confidence=0.97,
        reasoning="The document contains PAN information.",
    )

    service = DocumentProcessingService(
        document_type_detector=FakeDocumentTypeDetector(classification),
        extractors={
            DocumentType.PAN: FakePANExtractor(),
        },
    )

    detected_type, extracted_data = service.process(str(pdf_path))

    assert detected_type == classification
    assert isinstance(extracted_data, PANDocument)
    assert extracted_data.pan_number == "ABCDE1234F"
    assert extracted_data.holder_name == "ABC Technologies Pvt Ltd"


def test_document_processing_service_returns_none_for_other_document(tmp_path):
    pdf_path = tmp_path / "unknown.pdf"
    create_pdf(pdf_path)

    classification = DocumentTypeResult(
        document_type=DocumentType.OTHER,
        confidence=0.91,
        reasoning="The document does not match a supported document type.",
    )

    service = DocumentProcessingService(
        document_type_detector=FakeDocumentTypeDetector(classification),
        extractors={},
    )

    detected_type, extracted_data = service.process(str(pdf_path))

    assert detected_type.document_type == DocumentType.OTHER
    assert extracted_data is None