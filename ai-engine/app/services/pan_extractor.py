from app.models.pan import PANDocument
from app.services.base_extractor import BaseDocumentExtractor


class PANExtractor(BaseDocumentExtractor):
    """Extract structured PAN information from a PAN document."""

    @property
    def response_model(self) -> type[PANDocument]:
        return PANDocument

    def build_prompt(self, text: str) -> str:
        return f"""
You are a government procurement document verification assistant.

Analyze the following PAN document.

Extract only the information required by the PANDocument schema.

Rules:
- Do not invent information.
- If information is not present, use null where allowed.
- Preserve the PAN number exactly as shown on the document.
- Preserve the holder name exactly as shown.
- Identify the document type.
- Give a confidence score between 0 and 1.
- Add a warning if the PAN number or holder name is unclear,
  unreadable, or appears incomplete.
- Do not decide whether the PAN is valid or whether the bidder
  satisfies a tender requirement.
- PAN validity must be established through an authoritative
  verification source, not inferred solely from the document.

PAN DOCUMENT TEXT:
{text}
""".strip()