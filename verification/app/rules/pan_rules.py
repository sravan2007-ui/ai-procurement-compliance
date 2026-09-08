import re
from app.schemas.enums import VerificationStatus
from app.schemas.verification_result import VerificationResult
from app.schemas.verification_request import ExtractedData, BidderData, TenderRequirements
from app.adapters.pan_adapter import pan_adapter

PAN_REGEX = re.compile(r"^[A-Z]{5}[0-9]{4}[A-Z]{1}$")


def verify_pan(extracted: ExtractedData, bidder: BidderData, requirements: TenderRequirements) -> VerificationResult:
    if not requirements.pan_required:
        return VerificationResult(check_type="PAN", status=VerificationStatus.NOT_APPLICABLE,
                                   message="PAN verification not required for this tender.")

    pan_data = extracted.pan
    if not pan_data or not pan_data.pan_number:
        return VerificationResult(check_type="PAN", status=VerificationStatus.FAIL,
                                   message="PAN document/data not provided by bidder.")

    if not PAN_REGEX.match(pan_data.pan_number):
        return VerificationResult(check_type="PAN", status=VerificationStatus.FAIL,
                                   message="PAN format is invalid.", evidence={"pan_number": pan_data.pan_number})

    record = pan_adapter.get_record(pan_data.pan_number)
    if not record:
        return VerificationResult(check_type="PAN", status=VerificationStatus.MANUAL_REVIEW,
                                   message="PAN not found in government records.",
                                   evidence={"pan_number": pan_data.pan_number})

    if record["status"] != "VALID":
        return VerificationResult(check_type="PAN", status=VerificationStatus.FAIL,
                                   message=f"PAN status is {record['status']}.", evidence=record)

    # Note: the extracted PAN schema carries an individual's name/DOB/father's
    # name (PAN cards are issued to persons, not companies) - so we only
    # cross-check it against the government record itself, not the bidder's
    # company name, to avoid false-flagging a legitimate proprietor/director PAN.
    doc_name = (pan_data.name or "").strip().lower()
    if doc_name and doc_name != record["legal_name"].strip().lower():
        return VerificationResult(check_type="PAN", status=VerificationStatus.WARNING,
                                   message="Extracted PAN holder name does not match the government record.",
                                   score=70, evidence=record)

    return VerificationResult(check_type="PAN", status=VerificationStatus.PASS,
                               message="PAN is valid and matches government records.", score=100, evidence=record)
