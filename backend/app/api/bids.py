from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.bidder import Bidder
from app.models.tender import Tender
from app.models.tender_bid import TenderBid
from app.schemas.bid import BidCreate, BidResponse


router = APIRouter(
    prefix="/api/bids",
    tags=["Bids"],
)


@router.post("/", response_model=BidResponse)
def create_bid(
    bid: BidCreate,
    db: Session = Depends(get_db),
):
    tender = (
        db.query(Tender)
        .filter(Tender.id == bid.tender_id)
        .first()
    )

    if not tender:
        raise HTTPException(
            status_code=404,
            detail="Tender not found",
        )

    bidder = (
        db.query(Bidder)
        .filter(Bidder.id == bid.bidder_id)
        .first()
    )

    if not bidder:
        raise HTTPException(
            status_code=404,
            detail="Bidder not found",
        )

    new_bid = TenderBid(
        tender_id=bid.tender_id,
        bidder_id=bid.bidder_id,
        status="SUBMITTED",
    )

    db.add(new_bid)
    db.commit()
    db.refresh(new_bid)

    return new_bid