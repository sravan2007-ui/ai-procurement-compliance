import pytest

from app.models.compliance import ComplianceRule
from app.models.tender_requirement import TenderRequirement
from app.services.rules.tender_rule_builder import TenderRuleBuilder


def test_build_tender_requirement_into_compliance_rule():
    requirement = TenderRequirement(
        rule_id="GST_001",
        name="GST Status",
        description="GST registration must be active.",
        rule_type="GST_STATUS",
        parameters={
            "required_status": "Active",
        },
        mandatory=True,
        source_text="GST registration must be active.",
    )

    rule = TenderRuleBuilder().build(requirement)

    assert isinstance(rule, ComplianceRule)
    assert rule.rule_id == "GST_001"
    assert rule.name == "GST Status"
    assert rule.rule_type == "GST_STATUS"
    assert rule.parameters["required_status"] == "Active"
    assert rule.mandatory is True


def test_build_all_tender_requirements():
    requirements = [
        TenderRequirement(
            rule_id="GST_001",
            name="GST Status",
            description="GST must be active.",
            rule_type="GST_STATUS",
            parameters={"required_status": "Active"},
        ),
        TenderRequirement(
            rule_id="UDYAM_001",
            name="Udyam Eligibility",
            description="Bidder must have eligible Udyam classification.",
            rule_type="UDYAM_ELIGIBILITY",
            parameters={
                "allowed_types": ["Micro", "Small", "Medium"],
            },
        ),
    ]

    rules = TenderRuleBuilder().build_all(requirements)

    assert len(rules) == 2
    assert rules[0].rule_id == "GST_001"
    assert rules[0].rule_type == "GST_STATUS"
    assert rules[1].rule_id == "UDYAM_001"
    assert rules[1].rule_type == "UDYAM_ELIGIBILITY"


def test_build_rejects_unsupported_rule_type():
    requirement = TenderRequirement(
        rule_id="UNKNOWN_001",
        name="Unknown Requirement",
        description="Unsupported requirement.",
        rule_type="UNKNOWN_RULE",
    )

    with pytest.raises(
        ValueError,
        match="Unsupported rule type: UNKNOWN_RULE",
    ):
        TenderRuleBuilder().build(requirement)