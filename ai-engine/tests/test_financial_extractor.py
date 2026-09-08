import pymupdf

from app.models.financial import FinancialDocument
from app.services.document_extractor import DocumentExtractor
from app.services.financial_extractor import FinancialExtractor


class FakeGeminiClient:
    """Fake Gemini client used for unit testing."""

    def generate_structured(self, prompt, response_model):
        return response_model(
            company_name="ABC Technologies Pvt Ltd",
            financial_years=[
                {
                    "financial_year": "2023-24",
                    "turnover": 12.4,
                    "currency": "INR",
                },
                {
                    "financial_year": "2024-25",
                    "turnover": 14.1,
                    "currency": "INR",
                },
                {
                    "financial_year": "2025-26",
                    "turnover": 16.8,
                    "currency": "INR",
                },
            ],
            auditor_name="XYZ & Associates",
            certificate_date="2026-05-10",
            document_type="CA_TURNOVER_CERTIFICATE",
            raw_text=None,
            confidence=0.95,
            warnings=[],
        )


def test_financial_extractor(tmp_path):
    pdf_path = tmp_path / "turnover_certificate.pdf"

    document = pymupdf.open()
    page = document.new_page()

    page.insert_text(
        (72, 72),
        "Company: ABC Technologies Pvt Ltd\n"
        "FY 2023-24 Turnover: INR 12.4 Crore\n"
        "FY 2024-25 Turnover: INR 14.1 Crore\n"
        "FY 2025-26 Turnover: INR 16.8 Crore\n"
        "Auditor: XYZ & Associates",
    )

    document.save(pdf_path)
    document.close()

    extractor = FinancialExtractor(
        document_extractor=DocumentExtractor(),
        gemini_client=FakeGeminiClient(),
    )

    result = extractor.extract(str(pdf_path))

    assert isinstance(result, FinancialDocument)
    assert result.company_name == "ABC Technologies Pvt Ltd"
    assert len(result.financial_years) == 3
    assert result.financial_years[0].turnover == 12.4
    assert result.financial_years[1].turnover == 14.1
    assert result.financial_years[2].turnover == 16.8
    assert result.auditor_name == "XYZ & Associates"
    assert result.confidence == 0.95