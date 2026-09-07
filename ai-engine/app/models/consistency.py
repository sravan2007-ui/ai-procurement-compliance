from enum import Enum

from pydantic import BaseModel, Field


class ConsistencyStatus(str, Enum):
    CONSISTENT = "CONSISTENT"
    CONFLICT = "CONFLICT"
    REVIEW_REQUIRED = "REVIEW_REQUIRED"


class ConsistencyCheckResult(BaseModel):
    status: ConsistencyStatus
    field: str = Field(
        description="Field that was compared across documents."
    )
    message: str = Field(
        description="Human-readable explanation of the consistency result."
    )
    evidence: dict[str, str | None] = Field(
        default_factory=dict,
        description="Values found in the compared documents."
    )
    confidence: float = Field(
        ge=0.0,
        le=1.0,
        description="Confidence in the consistency check."
    )