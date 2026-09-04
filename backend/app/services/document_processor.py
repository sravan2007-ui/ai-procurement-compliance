from pathlib import Path

import pymupdf


def extract_text_from_pdf(file_path: str) -> str:
    """
    Extract text from a PDF document.

    Returns the combined text from all pages.
    """

    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(
            f"Document file not found: {file_path}"
        )

    document = pymupdf.open(path)

    try:
        pages = []

        for page in document:
            text = page.get_text()

            if text.strip():
                pages.append(text)

        return "\n".join(pages).strip()

    finally:
        document.close()