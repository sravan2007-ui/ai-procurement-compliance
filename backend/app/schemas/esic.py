from pydantic import BaseModel


class ESICExtractedData(BaseModel):
    employer_code: str | None = None
    establishment_name: str | None = None
    employer_name: str | None = None
    registration_date: str | None = None
    contribution_status: str | None = None
    compliance_period: str | None = None