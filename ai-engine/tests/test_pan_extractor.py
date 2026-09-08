import pymupdf

from app.models.pan import PANDocument
from app.services.pan_extractor import PANExtractor


class FakeGeminiClient:
    def generate_structured(self, prompt, response_model):
        assert response_model is PANDocument
        assert "PAN number exactly as shown" in prompt

        return PANDocument(
            pan_number="ABCDE1234F",
            holder_name="ABC Technologies Pvt Ltd",
            document_type="PAN Card",
            raw_text="sample PAN document",
            confidence=0.97,
            warnings=[],
        )


def test_pan_extractor_returns_structured_data(tmp_path):
    pdf_path = tmp_path / "pan.pdf"

    document = pymupdf.open()
    page = document.new_page()

    page.insert_text(
        (72, 72),
        "Permanent Account Number Card\n"
        "ABC Technologies Pvt Ltd\n"
        "ABCDE1234F",
    )

    document.save(pdf_path)
    document.close()

    extractor = PANExtractor(
        gemini_client=FakeGeminiClient(),
    )

    result = extractor.extract(str(pdf_path))

    assert isinstance(result, PANDocument)
    assert result.pan_number == "ABCDE1234F"
    assert result.holder_name == "ABC Technologies Pvt Ltd"
    assert result.document_type == "PAN Card"
    assert result.confidence == 0.97


def test_pan_extractor_rejects_empty_document(tmp_path):
    pdf_path = tmp_path / "empty_pan.pdf"

    document = pymupdf.open()
    document.new_page()
    document.save(pdf_path)
    document.close()

    extractor = PANExtractor(
        gemini_client=FakeGeminiClient(),
    )

    try:
        extractor.extract(str(pdf_path))
    except ValueError as exc:
        assert str(exc) == "No text could be extracted from the document."
    else:
        raise AssertionError("Expected ValueError for empty document")
