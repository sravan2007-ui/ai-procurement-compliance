from app.schemas.enums import VerificationStatus
from app.schemas.verification_result import VerificationResult
from app.schemas.verification_request import ExtractedData, BidderData, TenderRequirements
from app.adapters.startup_india_adapter import startup_india_adapter


def verify_startup_india(extracted: ExtractedData, bidder: BidderData,
                          requirements: TenderRequirements) -> VerificationResult:
    if not requirements.startup_india_required:
        return VerificationResult(check_type="STARTUP_INDIA", status=VerificationStatus.NOT_APPLICABLE,
                                   message="Startup India verification not required for this tender.")

    si_data = extracted.startup_india
    if not si_data or not si_data.certificate_number:
        return VerificationResult(check_type="STARTUP_INDIA", status=VerificationStatus.FAIL,
                                   message="Startup India certificate not provided.")

    record = startup_india_adapter.get_record(si_data.certificate_number)
    if not record:
        return VerificationResult(check_type="STARTUP_INDIA", status=VerificationStatus.MANUAL_REVIEW,
                                   message="Startup India certificate number not found in government records.",
                                   evidence={"certificate_number": si_data.certificate_number})

    if record.get("validity_status") != "VALID":
        return VerificationResult(check_type="STARTUP_INDIA", status=VerificationStatus.FAIL,
                                   message=f"Startup India certificate status is {record.get('validity_status')}.",
                                   evidence=record)

    if si_data.pan_number and record.get("pan_number") and si_data.pan_number != record["pan_number"]:
        return VerificationResult(check_type="STARTUP_INDIA", status=VerificationStatus.WARNING,
                                   message="PAN on the Startup India certificate does not match the extracted PAN.",
                                   score=60, evidence=record)

    company = bidder.company_name.strip().lower()
    if company != record.get("startup_name", "").strip().lower():
        return VerificationResult(check_type="STARTUP_INDIA", status=VerificationStatus.WARNING,
                                   message="Bidder's company name does not match the Startup India registration.",
                                   score=70, evidence=record)

    return VerificationResult(check_type="STARTUP_INDIA", status=VerificationStatus.PASS,
                               message="Startup India recognition is valid.", score=100, evidence=record)
