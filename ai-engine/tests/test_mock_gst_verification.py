from app.models.verification import VerificationStatus
from app.services.verification.mock_gst import MockGSTVerificationAdapter


def test_mock_gst_verification_succeeds():
    adapter = MockGSTVerificationAdapter(
        records={
            "29ABCDE1234F1Z5": {
                "gstin": "29ABCDE1234F1Z5",
                "legal_name": "ABC Pvt Ltd",
                "status": "Active",
            }
        }
    )

    result = adapter.verify("29ABCDE1234F1Z5")

    assert result.status == VerificationStatus.VERIFIED
    assert result.verified_data["legal_name"] == "ABC Pvt Ltd"


def test_mock_gst_verification_requires_review_when_record_is_unavailable():
    adapter = MockGSTVerificationAdapter(records={})

    result = adapter.verify("29UNKNOWN1234F1Z5")

    assert result.status == VerificationStatus.REVIEW_REQUIRED
    assert result.source == "MOCK_GST"