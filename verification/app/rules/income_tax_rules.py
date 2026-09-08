from app.schemas.enums import VerificationStatus
from app.schemas.verification_result import VerificationResult
from app.schemas.verification_request import ExtractedData, BidderData, TenderRequirements
from app.adapters.income_tax_adapter import income_tax_adapter


def verify_income_tax(extracted: ExtractedData, bidder: BidderData,
                       requirements: TenderRequirements) -> VerificationResult:
    if not requirements.income_tax_required:
        return VerificationResult(check_type="INCOME_TAX", status=VerificationStatus.NOT_APPLICABLE,
                                   message="Income Tax verification not required for this tender.")

    it_data = extracted.income_tax
    if not it_data or not it_data.pan_number:
        return VerificationResult(check_type="INCOME_TAX", status=VerificationStatus.FAIL,
                                   message="Income Tax return data not provided.")

    record = income_tax_adapter.get_record(it_data.pan_number)
    if not record:
        return VerificationResult(check_type="INCOME_TAX", status=VerificationStatus.MANUAL_REVIEW,
                                   message="No Income Tax record found for this PAN.",
                                   evidence={"pan_number": it_data.pan_number})

    if record.get("filing_status") != "FILED":
        return VerificationResult(check_type="INCOME_TAX", status=VerificationStatus.FAIL,
                                   message=f"Income Tax return filing status is {record.get('filing_status')}.",
                                   evidence=record)

    doc_name = (it_data.taxpayer_name or "").strip().lower()
    if doc_name and doc_name != record.get("taxpayer_name", "").strip().lower():
        return VerificationResult(check_type="INCOME_TAX", status=VerificationStatus.WARNING,
                                   message="Extracted taxpayer name does not match the government record.",
                                   score=70, evidence=record)

    return VerificationResult(check_type="INCOME_TAX", status=VerificationStatus.PASS,
                               message="Income Tax return has been filed and is on record.",
                               score=100, evidence=record)
