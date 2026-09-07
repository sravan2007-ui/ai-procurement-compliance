from app.models.udyam import UdyamDocument
from app.services.base_extractor import BaseDocumentExtractor


class UdyamExtractor(BaseDocumentExtractor):
    """Extract structured Udyam information from a Udyam document."""

    @property
    def response_model(self) -> type[UdyamDocument]:
        return UdyamDocument

    def build_prompt(self, text: str) -> str:
        return f"""
You are a government procurement document verification assistant.

Analyze the following Udyam Registration document text.

Extract only the information required by the UdyamDocument schema.

Rules:
- Do not invent information.
- If a field is not present, use null where allowed.
- Preserve the Udyam Registration Number exactly as written.
- Preserve the enterprise name exactly as written.
- Extract the organisation type if present.
- Extract the major activity if present.
- Extract the enterprise classification if present.
- Extract the registration date if present.
- Extract state and district if present.
- Give a confidence score between 0 and 1.
- Add a warning if important information is unclear or unreadable.

UDYAM DOCUMENT TEXT:
{text}
"""