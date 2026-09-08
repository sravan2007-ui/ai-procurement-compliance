from app.schemas.enums import VerificationStatus
from app.schemas.verification_result import VerificationResult
from app.schemas.verification_request import ExtractedData, BidderData, TenderRequirements
from app.adapters.blacklist_adapter import blacklist_adapter


def check_blacklist(extracted: ExtractedData, bidder: BidderData,
                     requirements: TenderRequirements) -> VerificationResult:
    if not requirements.blacklist_check_required:
        return VerificationResult(check_type="BLACKLIST", status=VerificationStatus.NOT_APPLICABLE,
                                   message="Blacklist check not required for this tender.")

    pan_number = extracted.pan.pan_number if extracted.pan else None
    gstin = extracted.gst.gstin if extracted.gst else None

    match, match_type = blacklist_adapter.find_match(pan_number, gstin, bidder.company_name)

    if match is None:
        return VerificationResult(check_type="BLACKLIST", status=VerificationStatus.PASS,
                                   message="Bidder not found in blacklist records.", score=100)

    if match_type == "FUZZY_NAME":
        # Not a confirmed hit - the name is suspiciously close to a blacklisted
        # entity but doesn't match on any hard identifier (PAN/GSTIN) or exact
        # name. Route to a human instead of silently failing or passing.
        return VerificationResult(
            check_type="BLACKLIST", status=VerificationStatus.MANUAL_REVIEW,
            message=("Bidder's name closely resembles a blacklisted entity "
                      f"(\"{match['entity_name']}\") but does not match exactly - manual verification required."),
            score=40, evidence=match,
        )

    return VerificationResult(
        check_type="BLACKLIST", status=VerificationStatus.FAIL,
        message=f"Bidder is blacklisted: {match.get('reason', 'No reason given')}.",
        score=0, evidence=match,
    )
