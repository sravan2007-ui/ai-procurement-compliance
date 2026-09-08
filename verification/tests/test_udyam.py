from app.rules.udyam_rules import verify_udyam
from app.schemas.verification_request import ExtractedData, TenderRequirements
from app.schemas.extracted_data import UdyamExtractedData
from app.schemas.enums import VerificationStatus


def test_udyam_valid_pass(clean_bidder):
    extracted = ExtractedData(udyam=UdyamExtractedData(udyam_number="UDYAM-AP-00-0000000",
                                                         enterprise_name="ABC Technologies Pvt Ltd"))
    result = verify_udyam(extracted, clean_bidder, TenderRequirements(udyam_required=True))
    assert result.status == VerificationStatus.PASS


def test_udyam_missing_fails(clean_bidder):
    result = verify_udyam(ExtractedData(), clean_bidder, TenderRequirements(udyam_required=True))
    assert result.status == VerificationStatus.FAIL


def test_udyam_not_required(clean_bidder):
    result = verify_udyam(ExtractedData(), clean_bidder, TenderRequirements(udyam_required=False))
    assert result.status == VerificationStatus.NOT_APPLICABLE
