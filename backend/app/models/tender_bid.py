from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class TenderBid(Base):
    __tablename__ = "tender_bids"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True,
    )

    tender_id: Mapped[int] = mapped_column(
        ForeignKey("tenders.id"),
        nullable=False,
        index=True,
    )

    bidder_id: Mapped[int] = mapped_column(
        ForeignKey("bidders.id"),
        nullable=False,
        index=True,
    )

    status: Mapped[str] = mapped_column(
        String(50),
        default="SUBMITTED",
        nullable=False,
    )

    submitted_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )