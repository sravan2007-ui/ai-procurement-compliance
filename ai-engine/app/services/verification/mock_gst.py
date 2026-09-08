from app.models.verification import (
    VerificationResult,
    VerificationStatus,
)
from app.services.verification.base import VerificationAdapter


class MockGSTVerificationAdapter(VerificationAdapter):
    """Mock GST verification provider for development and demonstration."""

    def __init__(self, records: dict[str, dict[str, str | None]] | None = None):
        self.records = records or {}

    def verify(self, identifier: str) -> VerificationResult:
        record = self.records.get(identifier)

        if record is None:
            return VerificationResult(
                status=VerificationStatus.REVIEW_REQUIRED,
                source="MOCK_GST",
                message="GST verification record is unavailable.",
                verified_data={},
                confidence=0.0,
            )

        return VerificationResult(
            status=VerificationStatus.VERIFIED,
            source="MOCK_GST",
            message="GSTIN was verified against the mock verification source.",
            verified_data=record,
            confidence=1.0,
        )