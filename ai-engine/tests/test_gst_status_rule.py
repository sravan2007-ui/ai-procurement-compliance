from app.models.compliance import (
    ComplianceRule,
    ComplianceStatus,
)
from app.models.gst import GSTDocument
from app.services.rules.gst_status_rule import GSTStatusRuleEvaluator


def test_gst_status_rule_passes_when_status_is_active():
    rule = ComplianceRule(
        rule_id="GST_STATUS_001",
        name="Active GST Registration",
        description="Bidder must have an active GST registration.",
        rule_type="GST_STATUS",
        parameters={
            "required_status": "Active",
        },
    )

    gst_document = GSTDocument(
        gstin="29ABCDE1234F1Z5",
        legal_name="ABC Pvt Ltd",
        status="Active",
        confidence=0.98,
    )

    evaluator = GSTStatusRuleEvaluator()

    result = evaluator.evaluate(rule, gst_document)

    assert result.status == ComplianceStatus.PASS
    assert result.evidence["actual_status"] == "Active"


def test_gst_status_rule_fails_when_status_is_cancelled():
    rule = ComplianceRule(
        rule_id="GST_STATUS_002",
        name="Active GST Registration",
        description="Bidder must have an active GST registration.",
        rule_type="GST_STATUS",
        parameters={
            "required_status": "Active",
        },
    )

    gst_document = GSTDocument(
        gstin="29ABCDE1234F1Z5",
        legal_name="ABC Pvt Ltd",
        status="Cancelled",
        confidence=0.98,
    )

    evaluator = GSTStatusRuleEvaluator()

    result = evaluator.evaluate(rule, gst_document)

    assert result.status == ComplianceStatus.FAIL
    assert result.evidence["actual_status"] == "Cancelled"


def test_gst_status_rule_requires_review_when_status_is_missing():
    rule = ComplianceRule(
        rule_id="GST_STATUS_003",
        name="Active GST Registration",
        description="Bidder must have an active GST registration.",
        rule_type="GST_STATUS",
        parameters={
            "required_status": "Active",
        },
    )

    gst_document = GSTDocument(
        gstin="29ABCDE1234F1Z5",
        legal_name="ABC Pvt Ltd",
        status=None,
        confidence=0.60,
    )

    evaluator = GSTStatusRuleEvaluator()

    result = evaluator.evaluate(rule, gst_document)

    assert result.status == ComplianceStatus.REVIEW_REQUIRED
    assert result.evidence["actual_status"] is None