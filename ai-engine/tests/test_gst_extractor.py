import pymupdf

from app.models.gst import GSTDocument
from app.services.document_extractor import DocumentExtractor
from app.services.gst_extractor import GSTExtractor


class FakeGeminiClient:
    """Fake Gemini client used for unit testing."""

    def generate_structured(self, prompt, response_model):
        return response_model(
            gstin="29ABCDE1234F1Z5",
            legal_name="ABC Technologies Pvt Ltd",
            trade_name="ABC Tech",
            registration_date="2021-04-12",
            status="Active",
            state="Karnataka",
            raw_text=None,
            confidence=0.97,
            warnings=[],
        )


def test_gst_extractor(tmp_path):
    pdf_path = tmp_path / "gst_certificate.pdf"

    document = pymupdf.open()
    page = document.new_page()

    page.insert_text(
        (72, 72),
        "GSTIN: 29ABCDE1234F1Z5\n"
        "Legal Name: ABC Technologies Pvt Ltd\n"
        "Status: Active\n"
        "State: Karnataka",
    )

    document.save(pdf_path)
    document.close()

    extractor = GSTExtractor(
        document_extractor=DocumentExtractor(),
        gemini_client=FakeGeminiClient(),
    )

    result = extractor.extract(str(pdf_path))

    assert isinstance(result, GSTDocument)
    assert result.gstin == "29ABCDE1234F1Z5"
    assert result.legal_name == "ABC Technologies Pvt Ltd"
    assert result.status == "Active"
    assert result.state == "Karnataka"
    assert result.confidence == 0.97