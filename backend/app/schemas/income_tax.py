from pydantic import BaseModel


class IncomeTaxExtractedData(BaseModel):
    pan_number: str | None = None
    taxpayer_name: str | None = None
    assessment_year: str | None = None
    filing_status: str | None = None
    return_filing_date: str | None = None
    gross_total_income: str | None = None
    taxable_income: str | None = None