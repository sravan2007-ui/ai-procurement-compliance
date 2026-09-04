from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.tender import Tender
from app.schemas.tender import TenderCreate, TenderResponse


router = APIRouter(
    prefix="/api/tenders",
    tags=["Tenders"],
)


@router.post("/", response_model=TenderResponse)
def create_tender(
    tender: TenderCreate,
    db: Session = Depends(get_db),
):
    new_tender = Tender(
        title=tender.title,
        organization=tender.organization,
        description=tender.description,
        submission_deadline=tender.submission_deadline,
        status="DRAFT",
    )

    db.add(new_tender)
    db.commit()
    db.refresh(new_tender)

    return new_tender


@router.get("/")
def get_tenders(
    db: Session = Depends(get_db),
):
    return db.query(Tender).all()