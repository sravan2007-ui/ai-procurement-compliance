import pymupdf

from app.models.document_type import DocumentType, DocumentTypeResult
from app.services.document_extractor import DocumentExtractor
from app.services.document_type_detector import DocumentTypeDetector


class FakeGeminiClient:
    """Fake Gemini client used for unit testing."""

    def generate_structured(self, prompt, response_model):
        return response_model(
            document_type=DocumentType.GST_CERTIFICATE,
            confidence=0.98,
            reasoning="The document contains a GSTIN and GST registration details.",
        )


def test_document_type_detector(tmp_path):
    pdf_path = tmp_path / "gst_certificate.pdf"

    document = pymupdf.open()
    page = document.new_page()

    page.insert_text(
        (72, 72),
        "GSTIN: 29ABCDE1234F1Z5\n"
        "Legal Name: ABC Technologies Pvt Ltd\n"
        "GST Registration Certificate\n"
        "Status: Active",
    )

    document.save(pdf_path)
    document.close()

    detector = DocumentTypeDetector(
        document_extractor=DocumentExtractor(),
        gemini_client=FakeGeminiClient(),
    )

    result = detector.detect(str(pdf_path))

    assert isinstance(result, DocumentTypeResult)
    assert result.document_type == DocumentType.GST_CERTIFICATE
    assert result.confidence == 0.98
    assert "GSTIN" in result.reasoning