from app.models.financial import FinancialDocument
from app.services.base_extractor import BaseDocumentExtractor


class FinancialExtractor(BaseDocumentExtractor):
    """Extract structured financial information from a financial document."""

    @property
    def response_model(self) -> type[FinancialDocument]:
        return FinancialDocument

    def build_prompt(self, text: str) -> str:
        return f"""
You are a government procurement document verification assistant.

Analyze the following financial document.

Extract only the information required by the FinancialDocument schema.

Rules:
- Do not invent financial information.
- If information is not present, use null where allowed.
- Extract the bidder/company name exactly as written.
- Extract every financial year and its corresponding turnover.
- Preserve the financial year exactly as written.
- Extract the currency if explicitly stated.
- Extract the auditor or Chartered Accountant name if present.
- Extract the certificate date if present.
- Identify the type of financial document.
- Give a confidence score between 0 and 1.
- Add a warning if a financial value, year, or other important information
  is unclear or unreadable.
- Do not calculate average turnover.
- Do not decide whether the bidder satisfies a tender requirement.

FINANCIAL DOCUMENT TEXT:
{text}
"""