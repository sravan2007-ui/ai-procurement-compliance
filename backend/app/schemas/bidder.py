from pydantic import BaseModel, EmailStr


class BidderCreate(BaseModel):
    company_name: str
    pan: str | None = None
    gstin: str | None = None
    udyam_number: str | None = None
    cin: str | None = None
    email: EmailStr | None = None
    phone: str | None = None


class BidderResponse(BidderCreate):
    id: int