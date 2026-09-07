from datetime import date

from pydantic import BaseModel, Field


class GSTDocument(BaseModel):
    """Structured information extracted from a GST registration document."""

    gstin: str = Field(
        description="15-character GST Identification Number."
    )

    legal_name: str = Field(
        description="Legal name of the registered business."
    )

    trade_name: str | None = Field(
        default=None,
        description="Trade name of the business, if available."
    )

    registration_date: date | None = Field(
        default=None,
        description="GST registration date."
    )

    status: str | None = Field(
        default=None,
        description="GST registration status, such as Active or Cancelled."
    )

    state: str | None = Field(
        default=None,
        description="State or Union Territory of registration."
    )

    raw_text: str | None = Field(
        default=None,
        description="Source text used for extraction."
    )

    confidence: float = Field(
        ge=0.0,
        le=1.0,
        description="AI confidence in the extracted GST information."
    )

    warnings: list[str] = Field(
        default_factory=list,
        description="Extraction warnings requiring attention."
    )