from pydantic import BaseModel


class GSTExtractedData(BaseModel):
    gstin: str | None = None
    legal_name: str | None = None
    trade_name: str | None = None
    registration_date: str | None = None
    business_type: str | None = None
    status: str | None = None
    principal_place_of_business: str | None = None