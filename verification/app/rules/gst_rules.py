import re
from app.schemas.enums import VerificationStatus
from app.schemas.verification_result import VerificationResult
from app.schemas.verification_request import ExtractedData, BidderData, TenderRequirements
from app.adapters.gst_adapter import gst_adapter

GSTIN_REGEX = re.compile(r"^[0-9]{2}[A-Z]{5}[0-9]{4}[A-Z]{1}[1-9A-Z]{1}Z[0-9A-Z]{1}$")


def verify_gst(extracted: ExtractedData, bidder: BidderData, requirements: TenderRequirements) -> VerificationResult:
    if not requirements.gst_required:
        return VerificationResult(check_type="GST", status=VerificationStatus.NOT_APPLICABLE,
                                   message="GST verification not required for this tender.")

    gst_data = extracted.gst
    if not gst_data or not gst_data.gstin:
        return VerificationResult(check_type="GST", status=VerificationStatus.FAIL,
                                   message="GST document/data not provided by bidder.")

    if not GSTIN_REGEX.match(gst_data.gstin):
        return VerificationResult(check_type="GST", status=VerificationStatus.FAIL,
                                   message="GSTIN format is invalid.", evidence={"gstin": gst_data.gstin})

    record = gst_adapter.get_record(gst_data.gstin)
    if not record:
        return VerificationResult(check_type="GST", status=VerificationStatus.MANUAL_REVIEW,
                                   message="GSTIN not found in government records.",
                                   evidence={"gstin": gst_data.gstin})

    if record["status"] != "ACTIVE":
        return VerificationResult(check_type="GST", status=VerificationStatus.FAIL,
                                   message=f"GST registration status is {record['status']}.", evidence=record)

    # Consistency check 1: does the extracted document actually say what the
    # government record says? (catches tampered/wrong documents)
    doc_name = (gst_data.legal_name or "").strip().lower()
    if doc_name and doc_name != record["legal_name"].strip().lower():
        return VerificationResult(check_type="GST", status=VerificationStatus.WARNING,
                                   message="Extracted GST document name does not match the government record.",
                                   score=60, evidence=record)

    # Consistency check 2: does this certificate actually belong to the
    # bidder submitting the bid? Accept a match against either legal or
    # trade name to avoid unnecessary false warnings.
    company = bidder.company_name.strip().lower()
    valid_names = {record["legal_name"].strip().lower()}
    if record.get("trade_name"):
        valid_names.add(record["trade_name"].strip().lower())
    if company not in valid_names:
        return VerificationResult(check_type="GST", status=VerificationStatus.WARNING,
                                   message="Bidder's declared company name does not match the GST legal/trade name.",
                                   score=70, evidence=record)

    if record.get("return_filing_status") != "COMPLIANT":
        return VerificationResult(check_type="GST", status=VerificationStatus.WARNING,
                                   message="GST return filing is not fully compliant.", score=75, evidence=record)

    return VerificationResult(check_type="GST", status=VerificationStatus.PASS,
                               message="GST registration is active and compliant.", score=100, evidence=record)
