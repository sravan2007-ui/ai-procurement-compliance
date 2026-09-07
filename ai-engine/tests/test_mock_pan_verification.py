from app.models.verification import VerificationStatus
from app.services.verification.mock_pan import MockPANVerificationAdapter


def test_mock_pan_verification_succeeds():
    adapter = MockPANVerificationAdapter(
        records={
            "ABCDE1234F": {
                "pan_number": "ABCDE1234F",
                "holder_name": "ABC Technologies Pvt Ltd",
                "status": "Active",
            }
        }
    )

    result = adapter.verify("ABCDE1234F")

    assert result.status == VerificationStatus.VERIFIED
    assert result.verified_data["holder_name"] == "ABC Technologies Pvt Ltd"


def test_mock_pan_verification_requires_review_when_record_is_unavailable():
    adapter = MockPANVerificationAdapter(records={})

    result = adapter.verify("UNKNOWN1234")

    assert result.status == VerificationStatus.REVIEW_REQUIRED
    assert result.source == "MOCK_PAN"