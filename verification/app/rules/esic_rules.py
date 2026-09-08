from app.schemas.enums import VerificationStatus
from app.schemas.verification_result import VerificationResult
from app.schemas.verification_request import ExtractedData, BidderData, TenderRequirements
from app.adapters.esic_adapter import esic_adapter


def verify_esic(extracted: ExtractedData, bidder: BidderData, requirements: TenderRequirements) -> VerificationResult:
    if not requirements.esic_required:
        return VerificationResult(check_type="ESIC", status=VerificationStatus.NOT_APPLICABLE,
                                   message="ESIC verification not required for this tender.")

    esic_data = extracted.esic
    if not esic_data or not esic_data.employer_code:
        return VerificationResult(check_type="ESIC", status=VerificationStatus.FAIL,
                                   message="ESIC employer code not provided.")

    record = esic_adapter.get_record(esic_data.employer_code)
    if not record:
        return VerificationResult(check_type="ESIC", status=VerificationStatus.MANUAL_REVIEW,
                                   message="ESIC employer code not found in government records.",
                                   evidence={"employer_code": esic_data.employer_code})

    if record.get("status") != "ACTIVE":
        return VerificationResult(check_type="ESIC", status=VerificationStatus.FAIL,
                                   message=f"ESIC registration status is {record.get('status')}.", evidence=record)

    company = bidder.company_name.strip().lower()
    if company != record.get("establishment_name", "").strip().lower():
        return VerificationResult(check_type="ESIC", status=VerificationStatus.WARNING,
                                   message="Bidder's company name does not match the ESIC establishment name.",
                                   score=70, evidence=record)

    if record.get("contribution_status") != "COMPLIANT":
        return VerificationResult(check_type="ESIC", status=VerificationStatus.WARNING,
                                   message="ESIC contributions are not fully compliant.", score=60, evidence=record)

    return VerificationResult(check_type="ESIC", status=VerificationStatus.PASS,
                               message="ESIC registration is active and contributions are compliant.",
                               score=100, evidence=record)
