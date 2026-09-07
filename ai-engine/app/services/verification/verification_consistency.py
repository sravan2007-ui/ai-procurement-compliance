from app.models.gst import GSTDocument
from app.models.verification import (
    VerificationResult,
    VerificationStatus,
)
from app.models.pan import PANDocument

class VerificationConsistencyChecker:
    """Compare submitted document data with verified source data."""

    def compare_gst(
        self,
        gst_document: GSTDocument,
        verification_result: VerificationResult,
    ) -> VerificationResult:

        if verification_result.status != VerificationStatus.VERIFIED:
            return verification_result

        verified_data = verification_result.verified_data

        verified_name = verified_data.get("legal_name")
        verified_status = verified_data.get("status")

        conflicts = []

        if (
            verified_name is not None
            and self._normalize(gst_document.legal_name)
            != self._normalize(verified_name)
        ):
            conflicts.append("legal_name")

        if (
            verified_status is not None
            and self._normalize(gst_document.status)
            != self._normalize(verified_status)
        ):
            conflicts.append("status")

        if conflicts:
            return VerificationResult(
                status=VerificationStatus.CONFLICT,
                source=verification_result.source,
                message=(
                    "Submitted GST document data conflicts with "
                    "the verification source."
                ),
                verified_data={
                    **verified_data,
                    "conflicting_fields": ", ".join(conflicts),
                },
                confidence=1.0,
            )

        return VerificationResult(
            status=VerificationStatus.VERIFIED,
            source=verification_result.source,
            message=(
                "Submitted GST document data is consistent "
                "with the verification source."
            ),
            verified_data=verified_data,
            confidence=1.0,
        )

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
    def compare_pan(
        self,
        pan_document,
        verification_result: VerificationResult,
    ) -> VerificationResult:

        if verification_result.status != VerificationStatus.VERIFIED:
            return verification_result

        verified_data = verification_result.verified_data

        verified_pan = verified_data.get("pan_number")
        verified_name = verified_data.get("holder_name")

        conflicts = []

        if (
            verified_pan is not None
            and self._normalize(pan_document.pan_number)
            != self._normalize(verified_pan)
        ):
            conflicts.append("pan_number")

        if (
            verified_name is not None
            and self._normalize(pan_document.holder_name)
            != self._normalize(verified_name)
        ):
            conflicts.append("holder_name")

        if conflicts:
            return VerificationResult(
                status=VerificationStatus.CONFLICT,
                source=verification_result.source,
                message=(
                    "Submitted PAN document data conflicts with "
                    "the verification source."
                ),
                verified_data={
                    **verified_data,
                    "conflicting_fields": ", ".join(conflicts),
                },
                confidence=1.0,
            )

        return VerificationResult(
            status=VerificationStatus.VERIFIED,
            source=verification_result.source,
            message=(
                "Submitted PAN document data is consistent "
                "with the verification source."
            ),
            verified_data=verified_data,
            confidence=1.0,
        )

    @staticmethod
    def _normalize(value: str | None) -> str:
        if not value:
            return ""

        return " ".join(
            value.lower()
            .replace(".", "")
            .replace(",", "")
            .split()
        )