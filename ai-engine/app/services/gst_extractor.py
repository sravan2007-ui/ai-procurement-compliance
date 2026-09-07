from app.models.gst import GSTDocument
from app.services.base_extractor import BaseDocumentExtractor


class GSTExtractor(BaseDocumentExtractor):
    """Extract structured GST information from a GST document."""

    @property
    def response_model(self) -> type[GSTDocument]:
        return GSTDocument

    def build_prompt(self, text: str) -> str:
        return f"""
You are a government procurement document verification assistant.

Analyze the following GST registration document text.

Extract only the information required by the GSTDocument schema.

Rules:
- Do not invent information.
- If a field is not present, use null where allowed.
- Preserve the GSTIN exactly as written.
- Preserve the legal name exactly as written.
- Identify the registration status if present.
- Extract the registration date if present.
- Identify the state if present.
- Give a confidence score between 0 and 1.
- Add a warning if important information is unclear or unreadable.

GST DOCUMENT TEXT:
{text}
"""