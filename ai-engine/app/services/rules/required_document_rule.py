from typing import Any

from app.models.compliance import (
    ComplianceResult,
    ComplianceRule,
    ComplianceStatus,
)


class RequiredDocumentRuleEvaluator:
    """Evaluate whether a required document has been submitted."""

    def evaluate(
        self,
        rule: ComplianceRule,
        submitted_documents: list[Any] | None,
    ) -> ComplianceResult:

        required_document_type = rule.parameters.get("document_type")

        if not required_document_type:
            return ComplianceResult(
                rule_id=rule.rule_id,
                status=ComplianceStatus.REVIEW_REQUIRED,
                message="Required document type is not specified.",
                evidence={},
                confidence=1.0,
            )

        if submitted_documents is None:
            submitted_documents = []
        elif isinstance(submitted_documents, dict):
            if "documents" in submitted_documents:
                submitted_documents = submitted_documents["documents"]
            else:
                submitted_documents = [submitted_documents]
        elif isinstance(submitted_documents, str):
            submitted_documents = [submitted_documents]

        submitted_types = []

        for document in submitted_documents:
            if isinstance(document, str):
                submitted_types.append(document)
            elif isinstance(document, dict):
                document_type = document.get("document_type")
                if document_type:
                    submitted_types.append(document_type)
            else:
                document_type = getattr(document, "document_type", None)
                if document_type:
                    submitted_types.append(document_type)

        if required_document_type in submitted_types:
            return ComplianceResult(
                rule_id=rule.rule_id,
                status=ComplianceStatus.PASS,
                message=(
                    f"Required document "
                    f"'{required_document_type}' has been submitted."
                ),
                evidence={
                    "required_document_type": required_document_type,
                    "submitted_document_types": submitted_types,
                },
                confidence=1.0,
            )

        return ComplianceResult(
            rule_id=rule.rule_id,
            status=ComplianceStatus.FAIL,
            message=(
                f"Required document "
                f"'{required_document_type}' has not been submitted."
            ),
            evidence={
                "required_document_type": required_document_type,
                "submitted_document_types": submitted_types,
            },
            confidence=1.0,
        )