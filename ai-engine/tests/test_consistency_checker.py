from app.models.consistency import ConsistencyStatus
from app.models.gst import GSTDocument
from app.models.udyam import UdyamDocument
from app.services.consistency_checker import ConsistencyChecker


def test_company_names_are_consistent():
    gst_document = GSTDocument(
        gstin="29ABCDE1234F1Z5",
        legal_name="ABC Pvt. Ltd.",
        confidence=0.98,
    )

    udyam_document = UdyamDocument(
        udyam_number="UDYAM-KA-01-1234567",
        enterprise_name="ABC Pvt Ltd",
        confidence=0.97,
    )

    checker = ConsistencyChecker()

    result = checker.compare_company_names(
        gst_document,
        udyam_document,
    )

    assert result.status == ConsistencyStatus.CONSISTENT


def test_company_names_conflict():
    gst_document = GSTDocument(
        gstin="29ABCDE1234F1Z5",
        legal_name="ABC Pvt Ltd",
        confidence=0.98,
    )

    udyam_document = UdyamDocument(
        udyam_number="UDYAM-KA-01-1234567",
        enterprise_name="XYZ Enterprises",
        confidence=0.97,
    )

    checker = ConsistencyChecker()

    result = checker.compare_company_names(
        gst_document,
        udyam_document,
    )

    assert result.status == ConsistencyStatus.CONFLICT
    assert result.evidence["gst_name"] == "ABC Pvt Ltd"
    assert result.evidence["udyam_name"] == "XYZ Enterprises"


def test_company_names_require_review_when_name_is_missing():
    gst_document = GSTDocument(
        gstin="29ABCDE1234F1Z5",
        legal_name="",
        confidence=0.60,
    )

    udyam_document = UdyamDocument(
        udyam_number="UDYAM-KA-01-1234567",
        enterprise_name="ABC Pvt Ltd",
        confidence=0.97,
    )

    checker = ConsistencyChecker()

    result = checker.compare_company_names(
        gst_document,
        udyam_document,
    )

    assert result.status == ConsistencyStatus.REVIEW_REQUIRED