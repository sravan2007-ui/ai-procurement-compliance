from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class Bidder(Base):
    __tablename__ = "bidders"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True,
    )

    company_name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    pan: Mapped[str | None] = mapped_column(
        String(20),
        nullable=True,
        index=True,
    )

    gstin: Mapped[str | None] = mapped_column(
        String(20),
        nullable=True,
        index=True,
    )

    udyam_number: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True,
        index=True,
    )

    cin: Mapped[str | None] = mapped_column(
        String(30),
        nullable=True,
        index=True,
    )

    email: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    phone: Mapped[str | None] = mapped_column(
        String(20),
        nullable=True,
    )