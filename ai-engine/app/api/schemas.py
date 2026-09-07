from typing import Any
from datetime import date
from pydantic import BaseModel, Field
from app.models.assessment import ComplianceAssessment


class ComplianceAnalysisRequest(BaseModel):
    tender_text: str = Field(
        min_length=1,
        description="Tender text containing the procurement requirements.",
    )

    bidder_data: dict[str, Any] = Field(
        default_factory=dict,
        description="Structured bidder information used for compliance evaluation.",
    )

    reference_date: date | None = Field(
        default=None,
        description=(
            "Reference date used for time-based compliance evaluation."
        ),
    )

class ComplianceAnalysisResponse(BaseModel):
    """AI Engine response containing the compliance assessment."""

    assessment: ComplianceAssessment