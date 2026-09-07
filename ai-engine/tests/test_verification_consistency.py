from app.models.gst import GSTDocument
from app.models.verification import (
    VerificationResult,
    VerificationStatus,
)
from app.services.verification.verification_consistency import (
    VerificationConsistencyChecker,
)
from app.models.pan import PANDocument

def test_gst_document_matches_verified_data():
    gst_document = GSTDocument(
        gstin="29ABCDE1234F1Z5",
        legal_name="ABC Pvt. Ltd.",
        status="Active",
        confidence=0.98,
    )

    verification_result = VerificationResult(
        status=VerificationStatus.VERIFIED,
        source="MOCK_GST",
        message="GSTIN verified.",
        verified_data={
            "gstin": "29ABCDE1234F1Z5",
            "legal_name": "ABC Pvt Ltd",
            "status": "Active",
        },
        confidence=1.0,
    )

    checker = VerificationConsistencyChecker()

    result = checker.compare_gst(
        gst_document,
        verification_result,
    )

    assert result.status == VerificationStatus.VERIFIED


def test_gst_document_conflicts_with_verified_data():
    gst_document = GSTDocument(
        gstin="29ABCDE1234F1Z5",
        legal_name="ABC Pvt Ltd",
        status="Active",
        confidence=0.98,
    )

    verification_result = VerificationResult(
        status=VerificationStatus.VERIFIED,
        source="MOCK_GST",
        message="GSTIN verified.",
        verified_data={
            "gstin": "29ABCDE1234F1Z5",
            "legal_name": "XYZ Enterprises",
            "status": "Cancelled",
        },
        confidence=1.0,
    )

    checker = VerificationConsistencyChecker()

    result = checker.compare_gst(
        gst_document,
        verification_result,
    )

    assert result.status == VerificationStatus.CONFLICT
    assert "legal_name" in result.verified_data["conflicting_fields"]
    assert "status" in result.verified_data["conflicting_fields"]


def test_gst_verification_unavailable_requires_review():
    gst_document = GSTDocument(
        gstin="29ABCDE1234F1Z5",
        legal_name="ABC Pvt Ltd",
        status="Active",
        confidence=0.98,
    )

    verification_result = VerificationResult(
        status=VerificationStatus.REVIEW_REQUIRED,
        source="MOCK_GST",
        message="GST verification record is unavailable.",
        verified_data={},
        confidence=0.0,
    )

    checker = VerificationConsistencyChecker()

    result = checker.compare_gst(
        gst_document,
        verification_result,
    )

    assert result.status == VerificationStatus.REVIEW_REQUIRED


def test_pan_document_matches_verified_data():
    pan_document = PANDocument(
        pan_number="ABCDE1234F",
        holder_name="ABC Pvt Ltd",
        document_type="PAN Card",
        confidence=0.98,
    )

    verification_result = VerificationResult(
        status=VerificationStatus.VERIFIED,
        source="MOCK_PAN",
        message="PAN verified.",
        verified_data={
            "pan_number": "ABCDE1234F",
            "holder_name": "ABC Pvt Ltd",
        },
        confidence=1.0,
    )

    checker = VerificationConsistencyChecker()

    result = checker.compare_pan(
        pan_document,
        verification_result,
    )

    assert result.status == VerificationStatus.VERIFIED


def test_pan_document_conflicts_with_verified_data():
    pan_document = PANDocument(
        pan_number="ABCDE1234F",
        holder_name="ABC Pvt Ltd",
        document_type="PAN Card",
        confidence=0.98,
    )

    verification_result = VerificationResult(
        status=VerificationStatus.VERIFIED,
        source="MOCK_PAN",
        message="PAN verified.",
        verified_data={
            "pan_number": "ABCDE1234F",
            "holder_name": "XYZ Enterprises",
        },
        confidence=1.0,
    )

    checker = VerificationConsistencyChecker()

    result = checker.compare_pan(
        pan_document,
        verification_result,
    )

    assert result.status == VerificationStatus.CONFLICT
    assert "holder_name" in result.verified_data["conflicting_fields"]


def test_pan_verification_unavailable_requires_review():
    pan_document = PANDocument(
        pan_number="ABCDE1234F",
        holder_name="ABC Pvt Ltd",
        document_type="PAN Card",
        confidence=0.98,
    )

    verification_result = VerificationResult(
        status=VerificationStatus.REVIEW_REQUIRED,
        source="MOCK_PAN",
        message="PAN verification record is unavailable.",
        verified_data={},
        confidence=0.0,
    )

    checker = VerificationConsistencyChecker()

    result = checker.compare_pan(
        pan_document,
        verification_result,
    )

    assert result.status == VerificationStatus.REVIEW_REQUIRED