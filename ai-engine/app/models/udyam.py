from datetime import date

from pydantic import BaseModel, Field


class UdyamDocument(BaseModel):
    """Structured information extracted from a Udyam registration document."""

    udyam_number: str = Field(
        description="Udyam Registration Number of the enterprise."
    )

    enterprise_name: str = Field(
        description="Name of the registered enterprise."
    )

    organisation_type: str | None = Field(
        default=None,
        description="Type of organisation, if available."
    )

    major_activity: str | None = Field(
        default=None,
        description="Major activity of the enterprise."
    )

    enterprise_type: str | None = Field(
        default=None,
        description="Enterprise classification such as Micro, Small, or Medium."
    )

    registration_date: date | None = Field(
        default=None,
        description="Udyam registration date."
    )

    state: str | None = Field(
        default=None,
        description="State or Union Territory of the enterprise."
    )

    district: str | None = Field(
        default=None,
        description="District of the enterprise."
    )

    raw_text: str | None = Field(
        default=None,
        description="Source text used for extraction."
    )

    confidence: float = Field(
        ge=0.0,
        le=1.0,
        description="AI confidence in the extracted information."
    )

    warnings: list[str] = Field(
        default_factory=list,
        description="Extraction warnings requiring attention."
    )