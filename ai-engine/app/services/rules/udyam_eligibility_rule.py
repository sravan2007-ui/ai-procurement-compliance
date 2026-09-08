from app.models.compliance import (
    ComplianceResult,
    ComplianceRule,
    ComplianceStatus,
)
from app.models.udyam import UdyamDocument


class UdyamEligibilityRuleEvaluator:
    """Evaluate whether the bidder's Udyam enterprise type is allowed."""

    def evaluate(
        self,
        rule: ComplianceRule,
        udyam_document: UdyamDocument | None,
    ) -> ComplianceResult:

        allowed_types = rule.parameters.get("allowed_types", [])

        if udyam_document is None:
            return ComplianceResult(
                rule_id=rule.rule_id,
                status=ComplianceStatus.REVIEW_REQUIRED,
                message="Udyam document was not provided.",
                evidence={
                    "enterprise_type": None,
                    "allowed_types": allowed_types,
                },
                confidence=1.0,
            )

        if isinstance(udyam_document, dict):
            try:
                udyam_document = UdyamDocument.model_validate(udyam_document)
            except Exception:
                return ComplianceResult(
                    rule_id=rule.rule_id,
                    status=ComplianceStatus.REVIEW_REQUIRED,
                    message="Submitted Udyam document could not be parsed.",
                    evidence={
                        "enterprise_type": None,
                        "allowed_types": allowed_types,
                    },
                    confidence=1.0,
                )

        actual_type = udyam_document.enterprise_type

        if not allowed_types:
            return ComplianceResult(
                rule_id=rule.rule_id,
                status=ComplianceStatus.REVIEW_REQUIRED,
                message="Allowed Udyam enterprise types are not specified.",
                evidence={
                    "enterprise_type": actual_type,
                    "allowed_types": allowed_types,
                },
                confidence=1.0,
            )

        if not actual_type:
            return ComplianceResult(
                rule_id=rule.rule_id,
                status=ComplianceStatus.REVIEW_REQUIRED,
                message="Udyam enterprise type is missing from the submitted document.",
                evidence={
                    "enterprise_type": None,
                    "allowed_types": allowed_types,
                },
                confidence=udyam_document.confidence,
            )

        normalized_actual = actual_type.strip().lower()
        normalized_allowed = [
            str(value).strip().lower()
            for value in allowed_types
        ]

        if normalized_actual in normalized_allowed:
            return ComplianceResult(
                rule_id=rule.rule_id,
                status=ComplianceStatus.PASS,
                message=(
                    f"Udyam enterprise type is '{actual_type}', "
                    "which is allowed by the tender requirement."
                ),
                evidence={
                    "enterprise_type": actual_type,
                    "allowed_types": allowed_types,
                },
                confidence=udyam_document.confidence,
            )

        return ComplianceResult(
            rule_id=rule.rule_id,
            status=ComplianceStatus.FAIL,
            message=(
                f"Udyam enterprise type is '{actual_type}', "
                "which is not allowed by the tender requirement."
            ),
            evidence={
                "enterprise_type": actual_type,
                "allowed_types": allowed_types,
            },
            confidence=udyam_document.confidence,
        )