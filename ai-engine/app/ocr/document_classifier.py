from typing import Tuple
from backend.app.schemas.document import DocumentType


class DocumentClassifier:
    """
    Classifies raw document text into standardized DocumentType enums.
    Uses multi-criteria weighted keyword and layout pattern detection.
    """

    @staticmethod
    def classify(text: str) -> Tuple[DocumentType, float]:
        text_lower = text.lower()

        # GST Certificate: Form GST REG-06
        if "gst reg-06" in text_lower or ("gstin" in text_lower and "registration certificate" in text_lower):
            return DocumentType.GST_CERTIFICATE, 0.98
        elif "gstin" in text_lower and "goods and services tax" in text_lower:
            return DocumentType.GST_CERTIFICATE, 0.92

        # PAN Card
        if "permanent account number" in text_lower and ("income tax department" in text_lower or "govt. of india" in text_lower):
            return DocumentType.PAN_CARD, 0.98

        # Udyam Certificate
        if "udyam registration certificate" in text_lower or ("udyam-" in text_lower and "ministry of micro" in text_lower):
            return DocumentType.UDYAM_CERTIFICATE, 0.98

        # Audited Financial Statements
        if ("balance sheet" in text_lower or "statement of profit and loss" in text_lower) and (
            "auditor" in text_lower or "chartered accountant" in text_lower or "udin" in text_lower
        ):
            return DocumentType.AUDITED_BALANCE_SHEET, 0.95

        # Make in India Declaration
        if "make in india" in text_lower and ("local content" in text_lower or "dpiit" in text_lower or "local supplier" in text_lower):
            return DocumentType.MAKE_IN_INDIA_DECLARATION, 0.96

        # Non-Blacklisting / Debarment Affidavit
        if ("affidavit" in text_lower or "undertaking" in text_lower) and (
            "blacklisted" in text_lower or "debarred" in text_lower or "non-blacklisting" in text_lower
        ):
            return DocumentType.NON_BLACKLISTING_AFFIDAVIT, 0.96

        # OEM Authorization
        if "oem" in text_lower and ("authorization" in text_lower or "letterhead" in text_lower or "manufacturer" in text_lower):
            return DocumentType.OEM_AUTHORIZATION, 0.92

        # Certificate of Incorporation
        if "certificate of incorporation" in text_lower or ("cin" in text_lower and "registrar of companies" in text_lower):
            return DocumentType.INCORPORATION_CERTIFICATE, 0.94

        return DocumentType.OTHER, 0.50


document_classifier = DocumentClassifier()
