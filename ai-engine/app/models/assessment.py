from enum import Enum
from pydantic import BaseModel, Field
from app.models.evidence import ComplianceEvidence
from app.models.compliance import ComplianceResult


class RiskLevel(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"


class ComplianceAssessment(BaseModel):
    overall_score: float = Field(...)
    risk_level: RiskLevel
    results: list[ComplianceResult] = Field(default_factory=list)
    evidence: list[ComplianceEvidence] = Field(
        default_factory=list,
        description="Evidence supporting each compliance evaluation.",
    )
    pass_count: int = Field(ge=0)
    fail_count: int = Field(ge=0)
    review_count: int = Field(ge=0)
    conflict_count: int = Field(ge=0)
    recommendation: str = Field(...)