from pydantic import BaseModel, Field


class PANDocument(BaseModel):
    """Structured information extracted from a PAN document."""

    pan_number: str | None = Field(
        default=None,
        description="PAN number exactly as shown on the document.",
    )
    holder_name: str | None = Field(
        default=None,
        description="Name of the PAN holder exactly as shown.",
    )
    document_type: str = Field(
        description="Type of PAN document.",
    )
    raw_text: str | None = Field(
        default=None,
        description="Source text used for extraction.",
    )
    confidence: float = Field(
        ge=0.0,
        le=1.0,
        description="AI confidence in the extracted PAN information.",
    )
    warnings: list[str] = Field(
        default_factory=list,
        description="Extraction warnings requiring attention.",
    )