from datetime import datetime
from pydantic import BaseModel

class BidCreate(BaseModel):
    tender_id: int
    bidder_id: int


class BidResponse(BaseModel):
    id: int
    tender_id: int
    bidder_id: int
    status: str
    submitted_at: datetime