from app.models.experience import ExperienceDocument
from app.services.base_extractor import BaseDocumentExtractor


class ExperienceExtractor(BaseDocumentExtractor):
    """Extract structured project experience from an experience document."""

    @property
    def response_model(self) -> type[ExperienceDocument]:
        return ExperienceDocument

    def build_prompt(self, text: str) -> str:
        return f"""
You are a government procurement document verification assistant.

Analyze the following experience certificate or project experience document.

Extract only the information required by the ExperienceDocument schema.

Rules:
- Do not invent information.
- If information is not present, use null where allowed.
- Preserve the bidder/company name exactly as written.
- Extract every project that is explicitly supported by the document.
- Preserve project names and client names exactly as written.
- Extract the project type if explicitly stated.
- Extract project value only when explicitly stated.
- Convert project values to INR crore.
- Examples:
  - 5 crore -> 5
  - ₹5 crore -> 5
  - 500 lakh -> 5
  - ₹50,000,000 -> 5
- Do not calculate project values.
- Extract the completion date when present.
- Do not treat an award date, start date, or contract date as a
  completion date unless the document explicitly identifies it as
  the completion date.
- Extract the document type.
- Give a confidence score between 0 and 1.
- Add a warning if project value, completion date, project type, or
  another important field is unclear or unreadable.
- Do not decide whether the bidder satisfies a tender experience
  requirement.

EXPERIENCE DOCUMENT TEXT:
{text}
""".strip()
