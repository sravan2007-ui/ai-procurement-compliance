from app.models.compliance import (
    ComplianceResult,
    ComplianceRule,
    ComplianceStatus,
)
from app.models.gst import GSTDocument


class GSTStatusRuleEvaluator:
    """Evaluate whether the bidder's GST registration has an acceptable status."""

    def evaluate(
        self,
        rule: ComplianceRule,
        gst_document: GSTDocument | None,
    ) -> ComplianceResult:

        required_status = rule.parameters.get("required_status", "Active")

        if gst_document is None:
            return ComplianceResult(
                rule_id=rule.rule_id,
                status=ComplianceStatus.REVIEW_REQUIRED,
                message="GST document was not provided.",
                evidence={
                    "actual_status": None,
                    "required_status": required_status,
                },
                confidence=1.0,
            )

        if isinstance(gst_document, dict):
            try:
                gst_document = GSTDocument.model_validate(gst_document)
            except Exception:
                return ComplianceResult(
                    rule_id=rule.rule_id,
                    status=ComplianceStatus.REVIEW_REQUIRED,
                    message="Submitted GST document could not be parsed.",
                    evidence={
                        "actual_status": None,
                        "required_status": required_status,
                    },
                    confidence=1.0,
                )

        actual_status = gst_document.status

        if not actual_status:
            return ComplianceResult(
                rule_id=rule.rule_id,
                status=ComplianceStatus.REVIEW_REQUIRED,
                message="GST registration status is missing from the submitted document.",
                evidence={
                    "gstin": gst_document.gstin,
                    "actual_status": None,
                    "required_status": required_status,
                },
                confidence=gst_document.confidence,
            )

        status_aliases = {
            "active": "valid",
            "valid": "valid",
            "inactive": "invalid",
            "cancelled": "invalid",
            "canceled": "invalid",
            "invalid": "invalid",
}

        normalized_actual_status = status_aliases.get(
            actual_status.strip().lower(),
            actual_status.strip().lower(),
        )

        normalized_required_status = status_aliases.get(
            required_status.strip().lower(),
            required_status.strip().lower(),
        )

        if normalized_actual_status == normalized_required_status:
            return ComplianceResult(
                rule_id=rule.rule_id,
                status=ComplianceStatus.PASS,
                message=(
                    f"GST registration status is '{actual_status}', "
                    f"which meets the required status '{required_status}'."
                ),
                evidence={
                    "gstin": gst_document.gstin,
                    "actual_status": actual_status,
                    "required_status": required_status,
                },
                confidence=gst_document.confidence,
            )

        return ComplianceResult(
            rule_id=rule.rule_id,
            status=ComplianceStatus.FAIL,
            message=(
                f"GST registration status is '{actual_status}', "
                f"which does not meet the required status '{required_status}'."
            ),
            evidence={
                "gstin": gst_document.gstin,
                "actual_status": actual_status,
                "required_status": required_status,
            },
            confidence=gst_document.confidence,
        )