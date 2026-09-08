from app.rules.esic_rules import verify_esic
from app.schemas.verification_request import ExtractedData, TenderRequirements
from app.schemas.extracted_data import ESICExtractedData
from app.schemas.enums import VerificationStatus


def test_esic_valid_pass(clean_bidder):
    extracted = ExtractedData(esic=ESICExtractedData(employer_code="ESIC12345",
                                                       establishment_name="ABC Technologies Pvt Ltd"))
    result = verify_esic(extracted, clean_bidder, TenderRequirements(esic_required=True))
    assert result.status == VerificationStatus.PASS


def test_esic_missing_fails(clean_bidder):
    result = verify_esic(ExtractedData(), clean_bidder, TenderRequirements(esic_required=True))
    assert result.status == VerificationStatus.FAIL
