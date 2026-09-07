
from typing import Any, TypedDict

from app.models.assessment import ComplianceAssessment
from app.models.compliance import ComplianceResult, ComplianceRule
from app.models.tender_requirement import TenderRequirement
from app.models.verification import VerificationResult


class ComplianceGraphState(TypedDict, total=False):
    """State carried through the AI compliance workflow."""

    tender_text: str
    bidder_data: dict[str, Any]
    reference_date: str | None

    requirements: list[TenderRequirement]
    rules: list[ComplianceRule]
    retrieved_knowledge: list[dict[str, Any]]

    verification_results: dict[str, VerificationResult]
    compliance_results: list[ComplianceResult]

    assessment: ComplianceAssessment | None

    error: str | None
