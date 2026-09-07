from enum import Enum

from pydantic import BaseModel, Field


class VerificationStatus(str, Enum):
    VERIFIED = "VERIFIED"
    CONFLICT = "CONFLICT"
    REVIEW_REQUIRED = "REVIEW_REQUIRED"


class VerificationResult(BaseModel):
    status: VerificationStatus
    source: str = Field(
        description="Authoritative or mock source used for verification."
    )
    message: str = Field(
        description="Human-readable explanation of the verification result."
    )
    verified_data: dict[str, str | None] = Field(
        default_factory=dict,
        description="Data returned or confirmed by the verification source.",
    )
    confidence: float = Field(
        ge=0.0,
        le=1.0,
        description="Confidence in the verification result.",
    )