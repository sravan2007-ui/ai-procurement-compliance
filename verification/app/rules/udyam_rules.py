from app.schemas.enums import VerificationStatus
from app.schemas.verification_result import VerificationResult
from app.schemas.verification_request import ExtractedData, BidderData, TenderRequirements
from app.adapters.udyam_adapter import udyam_adapter


def verify_udyam(extracted: ExtractedData, bidder: BidderData, requirements: TenderRequirements) -> VerificationResult:
    if not requirements.udyam_required:
        return VerificationResult(check_type="UDYAM", status=VerificationStatus.NOT_APPLICABLE,
                                   message="Udyam verification not required for this tender.")

    udyam_data = extracted.udyam
    if not udyam_data or not udyam_data.udyam_number:
        return VerificationResult(check_type="UDYAM", status=VerificationStatus.FAIL,
                                   message="Udyam registration document/data not provided.")

    record = udyam_adapter.get_record(udyam_data.udyam_number)
    if not record:
        return VerificationResult(check_type="UDYAM", status=VerificationStatus.MANUAL_REVIEW,
                                   message="Udyam number not found in government records.",
                                   evidence={"udyam_number": udyam_data.udyam_number})

    if record["status"] != "ACTIVE":
        return VerificationResult(check_type="UDYAM", status=VerificationStatus.FAIL,
                                   message=f"Udyam registration status is {record['status']}.", evidence=record)

    company = bidder.company_name.strip().lower()
    if company != record["enterprise_name"].strip().lower():
        return VerificationResult(check_type="UDYAM", status=VerificationStatus.WARNING,
                                   message="Bidder's declared company name does not match the Udyam enterprise name.",
                                   score=70, evidence=record)

    return VerificationResult(check_type="UDYAM", status=VerificationStatus.PASS,
                               message="Udyam registration is valid.", score=100, evidence=record)
