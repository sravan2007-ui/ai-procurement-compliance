from enum import Enum

from pydantic import BaseModel, Field


class DocumentType(str, Enum):
    GST_CERTIFICATE = "GST_CERTIFICATE"
    UDYAM_CERTIFICATE = "UDYAM_CERTIFICATE"
    PAN = "PAN"
    FINANCIAL_STATEMENT = "FINANCIAL_STATEMENT"
    EXPERIENCE_CERTIFICATE = "EXPERIENCE_CERTIFICATE"
    OTHER = "OTHER"


class DocumentTypeResult(BaseModel):
    """Result produced when classifying an uploaded document."""

    document_type: DocumentType

    confidence: float = Field(
        ge=0.0,
        le=1.0,
        description="AI confidence in the document classification.",
    )

    reasoning: str | None = Field(
        default=None,
        description="Short explanation for the classification.",
    )