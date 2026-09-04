from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.bidder import Bidder
from app.schemas.bidder import BidderCreate, BidderResponse


router = APIRouter(
    prefix="/api/bidders",
    tags=["Bidders"],
)


@router.post("/", response_model=BidderResponse)
def create_bidder(
    bidder: BidderCreate,
    db: Session = Depends(get_db),
):
    new_bidder = Bidder(
        company_name=bidder.company_name,
        pan=bidder.pan,
        gstin=bidder.gstin,
        udyam_number=bidder.udyam_number,
        cin=bidder.cin,
        email=bidder.email,
        phone=bidder.phone,
    )

    db.add(new_bidder)
    db.commit()
    db.refresh(new_bidder)

    return new_bidder


@router.get("/")
def get_bidders(
    db: Session = Depends(get_db),
):
    return db.query(Bidder).all()


@router.get("/{bidder_id}", response_model=BidderResponse)
def get_bidder(
    bidder_id: int,
    db: Session = Depends(get_db),
):
    bidder = (
        db.query(Bidder)
        .filter(Bidder.id == bidder_id)
        .first()
    )

    if not bidder:
        raise HTTPException(
            status_code=404,
            detail="Bidder not found",
        )

    return bidder