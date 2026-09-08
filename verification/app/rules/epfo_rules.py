from app.schemas.enums import VerificationStatus
from app.schemas.verification_result import VerificationResult
from app.schemas.verification_request import ExtractedData, BidderData, TenderRequirements
from app.adapters.epfo_adapter import epfo_adapter


def verify_epfo(extracted: ExtractedData, bidder: BidderData, requirements: TenderRequirements) -> VerificationResult:
    if not requirements.epfo_required:
        return VerificationResult(check_type="EPFO", status=VerificationStatus.NOT_APPLICABLE,
                                   message="EPFO verification not required for this tender.")

    epfo_data = extracted.epfo
    if not epfo_data or not epfo_data.establishment_id:
        return VerificationResult(check_type="EPFO", status=VerificationStatus.FAIL,
                                   message="EPFO establishment ID not provided.")

    record = epfo_adapter.get_record(epfo_data.establishment_id)
    if not record:
        return VerificationResult(check_type="EPFO", status=VerificationStatus.MANUAL_REVIEW,
                                   message="EPFO establishment not found in government records.",
                                   evidence={"establishment_id": epfo_data.establishment_id})

    if record.get("status") != "ACTIVE":
        return VerificationResult(check_type="EPFO", status=VerificationStatus.FAIL,
                                   message=f"EPFO establishment status is {record.get('status')}.", evidence=record)

    company = bidder.company_name.strip().lower()
    if company != record.get("establishment_name", "").strip().lower():
        return VerificationResult(check_type="EPFO", status=VerificationStatus.WARNING,
                                   message="Bidder's company name does not match the EPFO establishment name.",
                                   score=70, evidence=record)

    if record.get("contribution_status") != "COMPLIANT":
        return VerificationResult(check_type="EPFO", status=VerificationStatus.WARNING,
                                   message="EPFO contributions are not fully compliant.", score=60, evidence=record)

    return VerificationResult(check_type="EPFO", status=VerificationStatus.PASS,
                               message="EPFO registration is active and contributions are compliant.",
                               score=100, evidence=record)
