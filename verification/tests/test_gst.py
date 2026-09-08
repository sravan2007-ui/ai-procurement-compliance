from app.rules.gst_rules import verify_gst
from app.schemas.verification_request import ExtractedData, TenderRequirements, BidderData
from app.schemas.extracted_data import GSTExtractedData
from app.schemas.enums import VerificationStatus


def test_gst_valid_pass(clean_bidder):
    extracted = ExtractedData(gst=GSTExtractedData(gstin="37ABCDE1234F1Z5", legal_name="ABC Technologies Pvt Ltd"))
    result = verify_gst(extracted, clean_bidder, TenderRequirements(gst_required=True))
    assert result.status == VerificationStatus.PASS


def test_gst_not_required(clean_bidder):
    result = verify_gst(ExtractedData(), clean_bidder, TenderRequirements(gst_required=False))
    assert result.status == VerificationStatus.NOT_APPLICABLE


def test_gst_missing_data_fails(clean_bidder):
    result = verify_gst(ExtractedData(), clean_bidder, TenderRequirements(gst_required=True))
    assert result.status == VerificationStatus.FAIL


def test_gst_invalid_format_fails(clean_bidder):
    extracted = ExtractedData(gst=GSTExtractedData(gstin="NOTVALID"))
    result = verify_gst(extracted, clean_bidder, TenderRequirements(gst_required=True))
    assert result.status == VerificationStatus.FAIL


def test_gst_inactive_fails(blacklisted_bidder):
    extracted = ExtractedData(gst=GSTExtractedData(gstin="29XYZAB5678C1Z9", legal_name="XYZ Enterprises"))
    result = verify_gst(extracted, blacklisted_bidder, TenderRequirements(gst_required=True))
    assert result.status == VerificationStatus.FAIL


def test_gst_name_mismatch_warns():
    bidder = BidderData(bidder_id="B9", company_name="Totally Different Company")
    extracted = ExtractedData(gst=GSTExtractedData(gstin="37ABCDE1234F1Z5", legal_name="ABC Technologies Pvt Ltd"))
    result = verify_gst(extracted, bidder, TenderRequirements(gst_required=True))
    assert result.status == VerificationStatus.WARNING
