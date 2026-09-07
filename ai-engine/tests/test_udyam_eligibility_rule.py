from app.models.compliance import (
    ComplianceRule,
    ComplianceStatus,
)
from app.models.udyam import UdyamDocument
from app.services.rules.udyam_eligibility_rule import (
    UdyamEligibilityRuleEvaluator,
)


def test_udyam_rule_passes_when_enterprise_type_is_allowed():
    rule = ComplianceRule(
        rule_id="UDYAM_001",
        name="Udyam Enterprise Eligibility",
        description="Bidder must belong to an allowed enterprise category.",
        rule_type="UDYAM_ELIGIBILITY",
        parameters={
            "allowed_types": ["Small", "Medium"],
        },
    )

    udyam_document = UdyamDocument(
        udyam_number="UDYAM-KA-01-1234567",
        enterprise_name="ABC Pvt Ltd",
        enterprise_type="Small",
        confidence=0.97,
    )

    evaluator = UdyamEligibilityRuleEvaluator()

    result = evaluator.evaluate(rule, udyam_document)

    assert result.status == ComplianceStatus.PASS
    assert result.evidence["enterprise_type"] == "Small"


def test_udyam_rule_fails_when_enterprise_type_is_not_allowed():
    rule = ComplianceRule(
        rule_id="UDYAM_002",
        name="Udyam Enterprise Eligibility",
        description="Bidder must belong to an allowed enterprise category.",
        rule_type="UDYAM_ELIGIBILITY",
        parameters={
            "allowed_types": ["Small", "Medium"],
        },
    )

    udyam_document = UdyamDocument(
        udyam_number="UDYAM-KA-01-1234567",
        enterprise_name="ABC Pvt Ltd",
        enterprise_type="Micro",
        confidence=0.97,
    )

    evaluator = UdyamEligibilityRuleEvaluator()

    result = evaluator.evaluate(rule, udyam_document)

    assert result.status == ComplianceStatus.FAIL
    assert result.evidence["enterprise_type"] == "Micro"


def test_udyam_rule_requires_review_when_enterprise_type_is_missing():
    rule = ComplianceRule(
        rule_id="UDYAM_003",
        name="Udyam Enterprise Eligibility",
        description="Bidder must belong to an allowed enterprise category.",
        rule_type="UDYAM_ELIGIBILITY",
        parameters={
            "allowed_types": ["Small", "Medium"],
        },
    )

    udyam_document = UdyamDocument(
        udyam_number="UDYAM-KA-01-1234567",
        enterprise_name="ABC Pvt Ltd",
        enterprise_type=None,
        confidence=0.60,
    )

    evaluator = UdyamEligibilityRuleEvaluator()

    result = evaluator.evaluate(rule, udyam_document)

    assert result.status == ComplianceStatus.REVIEW_REQUIRED
    assert result.evidence["enterprise_type"] is None