from app.engine import run_verification
from app.schemas.verification_request import VerificationRequest, BidderData
from app.schemas.enums import OverallStatus, RiskLevel


def test_fully_compliant_bidder(clean_bidder, fully_compliant_extracted_data, all_required):
    request = VerificationRequest(
        tender_id="TND_001", bidder=clean_bidder,
        extracted_data=fully_compliant_extracted_data, requirements=all_required,
    )
    result = run_verification(request)
    assert result.overall_status == OverallStatus.COMPLIANT
    assert result.risk_level == RiskLevel.LOW
    assert result.compliance_score == 100.0
    assert all(r.status.value == "PASS" for r in result.verification_results)


def test_blacklisted_bidder_is_non_compliant_and_critical(fully_compliant_extracted_data, all_required):
    bidder = BidderData(bidder_id="B_FRAUD", company_name="Fraudulent Supplies Ltd")
    extracted = fully_compliant_extracted_data.model_copy()
    extracted.pan = extracted.pan.model_copy(update={"pan_number": "AABBC1122D"})
    request = VerificationRequest(tender_id="TND_002", bidder=bidder, extracted_data=extracted,
                                   requirements=all_required)
    result = run_verification(request)
    # Mandatory-check override: blacklist FAIL -> NON_COMPLIANT + CRITICAL,
    # regardless of every other check passing.
    assert result.overall_status == OverallStatus.NON_COMPLIANT
    assert result.risk_level == RiskLevel.CRITICAL
