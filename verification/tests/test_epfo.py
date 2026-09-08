from app.rules.epfo_rules import verify_epfo
from app.schemas.verification_request import ExtractedData, TenderRequirements
from app.schemas.extracted_data import EPFOExtractedData
from app.schemas.enums import VerificationStatus


def test_epfo_valid_pass(clean_bidder):
    extracted = ExtractedData(epfo=EPFOExtractedData(establishment_id="EPFO12345",
                                                       establishment_name="ABC Technologies Pvt Ltd"))
    result = verify_epfo(extracted, clean_bidder, TenderRequirements(epfo_required=True))
    assert result.status == VerificationStatus.PASS


def test_epfo_missing_fails(clean_bidder):
    result = verify_epfo(ExtractedData(), clean_bidder, TenderRequirements(epfo_required=True))
    assert result.status == VerificationStatus.FAIL


def test_epfo_not_found_manual_review(clean_bidder):
    extracted = ExtractedData(epfo=EPFOExtractedData(establishment_id="UNKNOWN999"))
    result = verify_epfo(extracted, clean_bidder, TenderRequirements(epfo_required=True))
    assert result.status == VerificationStatus.MANUAL_REVIEW
