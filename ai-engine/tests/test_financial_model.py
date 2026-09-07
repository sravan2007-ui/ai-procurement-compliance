from app.models.financial import FinancialDocument, FinancialYearTurnover


def test_financial_document():
    financial = FinancialDocument(
        company_name="ABC Technologies Pvt Ltd",
        financial_years=[
            FinancialYearTurnover(
                financial_year="2023-24",
                turnover=12.4,
            ),
            FinancialYearTurnover(
                financial_year="2024-25",
                turnover=14.1,
            ),
            FinancialYearTurnover(
                financial_year="2025-26",
                turnover=16.8,
            ),
        ],
        auditor_name="XYZ & Associates",
        certificate_date="2026-05-10",
        document_type="CA_TURNOVER_CERTIFICATE",
        confidence=0.95,
    )

    assert financial.company_name == "ABC Technologies Pvt Ltd"
    assert len(financial.financial_years) == 3
    assert financial.financial_years[0].turnover == 12.4
    assert financial.financial_years[1].financial_year == "2024-25"
    assert financial.auditor_name == "XYZ & Associates"
    assert financial.confidence == 0.95
    assert financial.warnings == []