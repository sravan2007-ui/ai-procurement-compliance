from app.models.compliance import (
    ComplianceRule,
    ComplianceStatus,
)
from app.services.rules.required_document_rule import (
    RequiredDocumentRuleEvaluator,
)


def test_required_document_rule_passes_when_document_is_present():
    rule = ComplianceRule(
        rule_id="DOC_GST_001",
        name="GST Certificate Required",
        description="Bidder must submit a GST certificate.",
        rule_type="REQUIRED_DOCUMENT",
        parameters={
            "document_type": "GST_CERTIFICATE",
        },
    )

    submitted_documents = [
        "GST_CERTIFICATE",
        "FINANCIAL_STATEMENT",
    ]

    evaluator = RequiredDocumentRuleEvaluator()

    result = evaluator.evaluate(rule, submitted_documents)

    assert result.status == ComplianceStatus.PASS
    assert result.evidence["required_document_type"] == "GST_CERTIFICATE"


def test_required_document_rule_fails_when_document_is_missing():
    rule = ComplianceRule(
        rule_id="DOC_GST_002",
        name="GST Certificate Required",
        description="Bidder must submit a GST certificate.",
        rule_type="REQUIRED_DOCUMENT",
        parameters={
            "document_type": "GST_CERTIFICATE",
        },
    )

    submitted_documents = [
        "FINANCIAL_STATEMENT",
        "UDYAM_CERTIFICATE",
    ]

    evaluator = RequiredDocumentRuleEvaluator()

    result = evaluator.evaluate(rule, submitted_documents)

    assert result.status == ComplianceStatus.FAIL
    assert result.evidence["required_document_type"] == "GST_CERTIFICATE"


def test_required_document_rule_requires_review_when_type_is_missing():
    rule = ComplianceRule(
        rule_id="DOC_001",
        name="Required Document",
        description="A required document must be submitted.",
        rule_type="REQUIRED_DOCUMENT",
        parameters={},
    )

    evaluator = RequiredDocumentRuleEvaluator()

    result = evaluator.evaluate(rule, [])

    assert result.status == ComplianceStatus.REVIEW_REQUIRED