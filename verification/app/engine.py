from typing import List
from app.schemas.enums import VerificationStatus, OverallStatus
from app.schemas.verification_request import VerificationRequest
from app.schemas.verification_result import VerificationResult, ComplianceResult
from app.rules.gst_rules import verify_gst
from app.rules.pan_rules import verify_pan
from app.rules.udyam_rules import verify_udyam
from app.rules.epfo_rules import verify_epfo
from app.rules.esic_rules import verify_esic
from app.rules.income_tax_rules import verify_income_tax
from app.rules.startup_india_rules import verify_startup_india
from app.rules.blacklist_rules import check_blacklist
from app.rules.local_content_rules import verify_local_content
from app.services.scoring_service import calculate_score
from app.services.risk_service import calculate_risk

# Checks that, if they FAIL, automatically make the bidder NON_COMPLIANT
# no matter how high the overall score is.
MANDATORY_FAILURE_CHECKS = {"BLACKLIST", "LOCAL_CONTENT"}


def _determine_overall_status(results: List[VerificationResult]) -> OverallStatus:
    for result in results:
        if result.check_type in MANDATORY_FAILURE_CHECKS and result.status == VerificationStatus.FAIL:
            return OverallStatus.NON_COMPLIANT

    if any(r.status == VerificationStatus.MANUAL_REVIEW for r in results):
        return OverallStatus.REVIEW_REQUIRED

    if any(r.status == VerificationStatus.FAIL for r in results):
        return OverallStatus.NON_COMPLIANT

    return OverallStatus.COMPLIANT


def run_verification(request: VerificationRequest) -> ComplianceResult:
    bidder = request.bidder
    extracted = request.extracted_data
    requirements = request.requirements

    results: List[VerificationResult] = [
        verify_gst(extracted, bidder, requirements),
        verify_pan(extracted, bidder, requirements),
        verify_udyam(extracted, bidder, requirements),
        verify_epfo(extracted, bidder, requirements),
        verify_esic(extracted, bidder, requirements),
        verify_income_tax(extracted, bidder, requirements),
        verify_startup_india(extracted, bidder, requirements),
        verify_local_content(extracted, bidder, requirements),
        check_blacklist(extracted, bidder, requirements),
    ]

    score = calculate_score(results)
    risk = calculate_risk(results, score)
    overall_status = _determine_overall_status(results)

    return ComplianceResult(
        bidder_id=bidder.bidder_id,
        tender_id=request.tender_id,
        verification_results=results,
        overall_status=overall_status,
        compliance_score=score,
        risk_level=risk,
    )
