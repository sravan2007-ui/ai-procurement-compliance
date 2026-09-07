from io import BytesIO

import fitz
import pytesseract
from PIL import Image


class OCRService:
    """Extract text from image-based PDF pages using Tesseract OCR."""

    def extract_page_text(self, page: fitz.Page) -> str:
        """Render a PDF page as an image and extract its text."""
        pixmap = page.get_pixmap(matrix=fitz.Matrix(2, 2), alpha=False)

        image = Image.open(BytesIO(pixmap.tobytes("png")))

        return pytesseract.image_to_string(image).strip()
