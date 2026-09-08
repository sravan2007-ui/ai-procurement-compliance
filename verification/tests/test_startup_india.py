from app.rules.startup_india_rules import verify_startup_india
from app.schemas.verification_request import ExtractedData, TenderRequirements
from app.schemas.extracted_data import StartupIndiaExtractedData
from app.schemas.enums import VerificationStatus


def test_startup_india_valid_pass(clean_bidder):
    extracted = ExtractedData(startup_india=StartupIndiaExtractedData(
        certificate_number="DIPP123456", pan_number="ABCDE1234F", startup_name="ABC Technologies Pvt Ltd"))
    result = verify_startup_india(extracted, clean_bidder, TenderRequirements(startup_india_required=True))
    assert result.status == VerificationStatus.PASS


def test_startup_india_missing_fails(clean_bidder):
    result = verify_startup_india(ExtractedData(), clean_bidder, TenderRequirements(startup_india_required=True))
    assert result.status == VerificationStatus.FAIL


def test_startup_india_pan_mismatch_warns(clean_bidder):
    extracted = ExtractedData(startup_india=StartupIndiaExtractedData(
        certificate_number="DIPP123456", pan_number="WRONGPAN1X", startup_name="ABC Technologies Pvt Ltd"))
    result = verify_startup_india(extracted, clean_bidder, TenderRequirements(startup_india_required=True))
    assert result.status == VerificationStatus.WARNING
