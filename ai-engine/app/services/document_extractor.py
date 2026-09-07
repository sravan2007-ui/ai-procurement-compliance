import fitz

from app.ocr.ocr_service import OCRService


class DocumentExtractor:
    """Extract text from text-based and scanned PDF documents."""

    def __init__(self, ocr_service=None) -> None:
        self.ocr_service = ocr_service or OCRService()

    def extract_text(self, file_path: str) -> str:
        """
        Extract text from all pages of a PDF.

        Uses the PDF text layer when available and falls back
        to OCR for image-only pages.
        """
        document = fitz.open(file_path)

        try:
            pages = []

            for page in document:
                text = page.get_text().strip()

                if text:
                    pages.append(text)
                else:
                    ocr_text = self.ocr_service.extract_page_text(page)

                    if ocr_text:
                        pages.append(ocr_text)

            return "\n".join(pages).strip()

        finally:
            document.close()