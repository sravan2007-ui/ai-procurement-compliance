from app.rules.pan_rules import verify_pan
from app.schemas.verification_request import ExtractedData, TenderRequirements
from app.schemas.extracted_data import PANExtractedData
from app.schemas.enums import VerificationStatus


def test_pan_valid_pass(clean_bidder):
    extracted = ExtractedData(pan=PANExtractedData(pan_number="ABCDE1234F", name="ABC Technologies Pvt Ltd"))
    result = verify_pan(extracted, clean_bidder, TenderRequirements(pan_required=True))
    assert result.status == VerificationStatus.PASS


def test_pan_missing_fails(clean_bidder):
    result = verify_pan(ExtractedData(), clean_bidder, TenderRequirements(pan_required=True))
    assert result.status == VerificationStatus.FAIL


def test_pan_invalid_format_fails(clean_bidder):
    extracted = ExtractedData(pan=PANExtractedData(pan_number="INVALID"))
    result = verify_pan(extracted, clean_bidder, TenderRequirements(pan_required=True))
    assert result.status == VerificationStatus.FAIL


def test_pan_not_found_manual_review(clean_bidder):
    extracted = ExtractedData(pan=PANExtractedData(pan_number="NOTFO1234U"))
    result = verify_pan(extracted, clean_bidder, TenderRequirements(pan_required=True))
    assert result.status == VerificationStatus.MANUAL_REVIEW
