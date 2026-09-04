from datetime import datetime
from pydantic import BaseModel

class TenderCreate(BaseModel):
    title: str
    organization: str
    description: str | None = None
    submission_deadline: datetime | None = None

class TenderResponse(TenderCreate):
    id: int
    status: str