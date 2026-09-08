from typing import Any, Dict, List
from pydantic import BaseModel, Field
from app.schemas.enums import VerificationStatus, OverallStatus, RiskLevel


class VerificationResult(BaseModel):
    check_type: str
    status: VerificationStatus
    message: str
    score: float = 0
    evidence: Dict[str, Any] = Field(default_factory=dict)


class ComplianceResult(BaseModel):
    bidder_id: str
    tender_id: str
    verification_results: List[VerificationResult]
    overall_status: OverallStatus
    compliance_score: float
    risk_level: RiskLevel
