from datetime import date

from pydantic import BaseModel, Field


class FinancialYearTurnover(BaseModel):
    """Turnover information for a single financial year."""

    financial_year: str = Field(
        description="Financial year, for example 2024-25."
    )

    turnover: float = Field(
        ge=0,
        description="Turnover for the financial year."
    )

    currency: str = Field(
        default="INR",
        description="Currency in which turnover is reported."
    )


class FinancialDocument(BaseModel):
    """Structured financial information extracted from a document."""

    company_name: str = Field(
        description="Name of the bidder or enterprise."
    )

    financial_years: list[FinancialYearTurnover] = Field(
        default_factory=list,
        description="Turnover reported for each financial year."
    )

    auditor_name: str | None = Field(
        default=None,
        description="Name of the auditor or Chartered Accountant, if available."
    )

    certificate_date: date | None = Field(
        default=None,
        description="Date of the financial certificate, if available."
    )

    document_type: str = Field(
        description="Type of financial document."
    )

    raw_text: str | None = Field(
        default=None,
        description="Source text used for extraction."
    )

    confidence: float = Field(
        ge=0.0,
        le=1.0,
        description="AI confidence in the extracted financial information."
    )

    warnings: list[str] = Field(
        default_factory=list,
        description="Extraction warnings requiring attention."
    )