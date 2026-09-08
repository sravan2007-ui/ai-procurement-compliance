from app.models.consistency import (
    ConsistencyCheckResult,
    ConsistencyStatus,
)
from app.models.gst import GSTDocument
from app.models.udyam import UdyamDocument


class ConsistencyChecker:
    """Check whether bidder information is consistent across documents."""

    def compare_company_names(
        self,
        gst_document: GSTDocument,
        udyam_document: UdyamDocument,
    ) -> ConsistencyCheckResult:

        gst_name = gst_document.legal_name
        udyam_name = udyam_document.enterprise_name

        if not gst_name or not udyam_name:
            return ConsistencyCheckResult(
                status=ConsistencyStatus.REVIEW_REQUIRED,
                field="company_name",
                message=(
                    "Company name could not be compared because "
                    "one or more documents are missing the name."
                ),
                evidence={
                    "gst_name": gst_name,
                    "udyam_name": udyam_name,
                },
                confidence=0.8,
            )

        normalized_gst_name = self._normalize_name(gst_name)
        normalized_udyam_name = self._normalize_name(udyam_name)

        if normalized_gst_name == normalized_udyam_name:
            return ConsistencyCheckResult(
                status=ConsistencyStatus.CONSISTENT,
                field="company_name",
                message="Company names match across GST and Udyam documents.",
                evidence={
                    "gst_name": gst_name,
                    "udyam_name": udyam_name,
                },
                confidence=1.0,
            )

        return ConsistencyCheckResult(
            status=ConsistencyStatus.CONFLICT,
            field="company_name",
            message=(
                "Company names differ between the GST and Udyam documents."
            ),
            evidence={
                "gst_name": gst_name,
                "udyam_name": udyam_name,
            },
            confidence=1.0,
        )

    @staticmethod
    def _normalize_name(name: str) -> str:
        """Normalize company names for basic comparison."""

        return " ".join(
            name.lower()
            .replace(".", "")
            .replace(",", "")
            .split()
        )