from app.rules.blacklist_rules import check_blacklist
from app.schemas.verification_request import ExtractedData, TenderRequirements, BidderData
from app.schemas.extracted_data import PANExtractedData, GSTExtractedData
from app.schemas.enums import VerificationStatus


def test_clean_bidder_passes(clean_bidder):
    extracted = ExtractedData(pan=PANExtractedData(pan_number="ABCDE1234F"))
    result = check_blacklist(extracted, clean_bidder, TenderRequirements())
    assert result.status == VerificationStatus.PASS


def test_blacklisted_pan_fails(blacklisted_bidder):
    extracted = ExtractedData(pan=PANExtractedData(pan_number="XYZAB5678C"))
    result = check_blacklist(extracted, blacklisted_bidder, TenderRequirements())
    assert result.status == VerificationStatus.FAIL


def test_blacklisted_gstin_fails(blacklisted_bidder):
    extracted = ExtractedData(gst=GSTExtractedData(gstin="29XYZAB5678C1Z9"))
    result = check_blacklist(extracted, blacklisted_bidder, TenderRequirements())
    assert result.status == VerificationStatus.FAIL


def test_regression_previously_missed_blacklist_entry_now_fails():
    """
    Regression test for the exact bug reported: bidder 'Fraudulent Supplies
    Ltd' / PAN 'AABBC1122D' was passing because that entity wasn't in the
    seed blacklist data. It has now been added - this must FAIL.
    """
    bidder = BidderData(bidder_id="B_FRAUD", company_name="Fraudulent Supplies Ltd")
    extracted = ExtractedData(pan=PANExtractedData(pan_number="AABBC1122D"))
    result = check_blacklist(extracted, bidder, TenderRequirements())
    assert result.status == VerificationStatus.FAIL


def test_fuzzy_name_match_flags_manual_review():
    """A near-identical (but not identical, and no matching PAN/GSTIN) name
    to a blacklisted entity should be routed to a human, not silently passed."""
    bidder = BidderData(bidder_id="B_SIMILAR", company_name="Fraudulent Supplies Limited")
    extracted = ExtractedData(pan=PANExtractedData(pan_number="UNRELATED9Z"))
    result = check_blacklist(extracted, bidder, TenderRequirements())
    assert result.status == VerificationStatus.MANUAL_REVIEW


def test_unrelated_company_passes():
    bidder = BidderData(bidder_id="B_OK", company_name="Sunshine Constructions Pvt Ltd")
    extracted = ExtractedData(pan=PANExtractedData(pan_number="UNRELATED9Z"))
    result = check_blacklist(extracted, bidder, TenderRequirements())
    assert result.status == VerificationStatus.PASS
