from app.models.verification import (
    VerificationResult,
    VerificationStatus,
)


def test_verification_result():
    result = VerificationResult(
        status=VerificationStatus.VERIFIED,
        source="MOCK_GST",
        message="GSTIN verified successfully.",
        verified_data={
            "gstin": "29ABCDE1234F1Z5",
            "legal_name": "ABC Pvt Ltd",
            "status": "Active",
        },
        confidence=1.0,
    )

    assert result.status == VerificationStatus.VERIFIED
    assert result.source == "MOCK_GST"
    assert result.verified_data["status"] == "Active"