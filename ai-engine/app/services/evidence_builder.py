from typing import Any

from app.models.compliance import ComplianceResult
from app.models.evidence import (
    ComplianceEvidence,
    EvidenceItem,
    EvidenceSourceType,
)
from app.models.verification import VerificationResult

class EvidenceBuilder:
    """Build audit evidence from compliance evaluation results."""

    def build(
    self,
    result: ComplianceResult,
    data: Any = None,
    verification: VerificationResult | None = None,
) -> ComplianceEvidence:
        items: list[EvidenceItem] = []

        if data is not None:
            items.extend(self._build_data_evidence(data))

        if verification is not None:
            items.extend(
                self._build_verification_evidence(verification)
            )

        items.append(
            EvidenceItem(
                source_type=EvidenceSourceType.RULE_ENGINE,
                source_name="Compliance Rule Engine",
                field="status",
                value=(
    result.status.value
    if hasattr(result.status, "value")
    else result.status
),
                description=(
                    f"Rule '{result.rule_id}' evaluated the supplied "
f"bidder information with status "
f"{result.status.value if hasattr(result.status, 'value') else result.status}."
                ),
            )
        )

        summary = self._build_summary(result, items)

        return ComplianceEvidence(
            rule_id=result.rule_id,
            items=items,
            summary=summary,
        )

    @staticmethod
    def _build_data_evidence(data: Any) -> list[EvidenceItem]:
        items: list[EvidenceItem] = []

        if isinstance(data, dict):
            for field, value in data.items():
                items.append(
                    EvidenceItem(
                        source_type=EvidenceSourceType.DOCUMENT,
                        source_name="Submitted Bidder Data",
                        field=field,
                        value=EvidenceBuilder._normalize_value(value),
                        description=(
                            f"Value for '{field}' was supplied as "
                            "bidder compliance data."
                        ),
                    )
                )
            return items

        if hasattr(data, "model_dump"):
            values = data.model_dump()

            for field, value in values.items():
                if field in {"raw_text", "warnings", "confidence"}:
                    continue

                items.append(
                    EvidenceItem(
                        source_type=EvidenceSourceType.DOCUMENT,
                        source_name=type(data).__name__,
                        field=field,
                        value=EvidenceBuilder._normalize_value(value),
                        description=(
                            f"Value for '{field}' was extracted from "
                            f"{type(data).__name__}."
                        ),
                    )
                )

        return items

    @staticmethod
    def _build_verification_evidence(
        verification: VerificationResult,
    ) -> list[EvidenceItem]:
        items: list[EvidenceItem] = []

        for field, value in verification.verified_data.items():
            items.append(
                EvidenceItem(
                    source_type=EvidenceSourceType.VERIFICATION_SOURCE,
                    source_name=verification.source,
                    field=field,
                    value=value,
                    description=(
                        f"Verification source returned '{field}' "
                        f"with value '{value}'."
                    ),
                )
            )

        items.append(
            EvidenceItem(
                source_type=EvidenceSourceType.VERIFICATION_SOURCE,
                source_name=verification.source,
                field="verification_status",
                value=verification.status.value,
                description=verification.message,
            )
        )

        return items

    @staticmethod
    def _normalize_value(
        value: Any,
    ) -> str | int | float | bool | None:
        if value is None or isinstance(
            value,
            (str, int, float, bool),
        ):
            return value

        return str(value)

    @staticmethod
    def _build_summary(
        result: ComplianceResult,
        items: list[EvidenceItem],
    ) -> str:
        if not items:
            return (
                f"No supporting evidence was available for rule "
                f"'{result.rule_id}'."
            )

        status = (
            result.status.value
            if hasattr(result.status, "value")
            else result.status
        )

        return (
            f"{len(items)} evidence item(s) support the evaluation "
            f"of rule '{result.rule_id}' with status "
            f"{status}."
        )