from app.rules.income_tax_rules import verify_income_tax
from app.schemas.verification_request import ExtractedData, TenderRequirements
from app.schemas.extracted_data import IncomeTaxExtractedData
from app.schemas.enums import VerificationStatus


def test_income_tax_filed_pass(clean_bidder):
    extracted = ExtractedData(income_tax=IncomeTaxExtractedData(pan_number="ABCDE1234F",
                                                                  taxpayer_name="ABC Technologies Pvt Ltd"))
    result = verify_income_tax(extracted, clean_bidder, TenderRequirements(income_tax_required=True))
    assert result.status == VerificationStatus.PASS


def test_income_tax_missing_fails(clean_bidder):
    result = verify_income_tax(ExtractedData(), clean_bidder, TenderRequirements(income_tax_required=True))
    assert result.status == VerificationStatus.FAIL
