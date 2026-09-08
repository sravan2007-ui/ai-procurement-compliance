import pymupdf

from app.services.document_extractor import DocumentExtractor


class FakeOCRService:
    """Return deterministic OCR text without calling Tesseract."""

    def extract_page_text(self, page):
        return "GSTIN: 29ABCDE1234F1Z5"


def test_document_extractor_extracts_text_pdf(tmp_path):
    pdf_path = tmp_path / "test_document.pdf"

    document = pymupdf.open()
    page = document.new_page()

    page.insert_text(
        (72, 72),
        "GSTIN: 29ABCDE1234F1Z5\n"
        "Legal Name: ABC Technologies Pvt Ltd\n"
        "Status: Active",
    )

    document.save(pdf_path)
    document.close()

    extractor = DocumentExtractor(
        ocr_service=FakeOCRService(),
    )

    text = extractor.extract_text(str(pdf_path))

    assert "GSTIN: 29ABCDE1234F1Z5" in text
    assert "ABC Technologies Pvt Ltd" in text
    assert "Status: Active" in text


def test_document_extractor_uses_ocr_for_scanned_page(tmp_path):
    pdf_path = tmp_path / "scanned_document.pdf"

    document = pymupdf.open()
    document.new_page()
    document.save(pdf_path)
    document.close()

    extractor = DocumentExtractor(
        ocr_service=FakeOCRService(),
    )

    text = extractor.extract_text(str(pdf_path))

    assert "GSTIN: 29ABCDE1234F1Z5" in text