from datetime import datetime, timezone

from pydantic import BaseModel, Field


class DocumentExtraction(BaseModel):
    """Structured result produced after AI document extraction."""

    document_type: str = Field(
        description="Type of document that was analyzed."
    )

    confidence: float = Field(
        ge=0.0,
        le=1.0,
        description="AI confidence in the extraction result."
    )

    extracted_text: str = Field(
        description="Raw text extracted from the document."
    )

    fields: dict[str, str | int | float | bool | None] = Field(
        default_factory=dict,
        description="Structured fields extracted from the document."
    )

    warnings: list[str] = Field(
        default_factory=list,
        description="Warnings or issues detected during extraction."
    )

    extracted_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )