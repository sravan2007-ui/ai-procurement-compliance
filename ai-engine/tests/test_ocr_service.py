import pymupdf

from app.ocr.ocr_service import OCRService


def test_ocr_service_extracts_text_from_image_pdf(tmp_path):
    pdf_path = tmp_path / "scanned_document.pdf"

    document = pymupdf.open()
    page = document.new_page(width=600, height=200)

    # Render text into an image so the PDF page contains no PDF text layer.
    text_page = document.new_page(width=600, height=200)
    text_page.insert_text(
        (72, 72),
        "GSTIN: 29ABCDE1234F1Z5",
        fontsize=24,
    )

    pixmap = text_page.get_pixmap(matrix=pymupdf.Matrix(2, 2), alpha=False)

    image_only_document = pymupdf.open()
    image_page = image_only_document.new_page(width=600, height=200)
    image_page.insert_image(
        pymupdf.Rect(0, 0, 600, 200),
        pixmap=pixmap,
    )

    image_only_document.save(pdf_path)

    document.close()
    image_only_document.close()

    scanned_document = pymupdf.open(pdf_path)
    scanned_page = scanned_document[0]

    text = OCRService().extract_page_text(scanned_page)

    scanned_document.close()

    assert "GSTIN" in text.upper()