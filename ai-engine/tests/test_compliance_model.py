from app.models.compliance import (
    ComplianceResult,
    ComplianceRule,
    ComplianceStatus,
)


def test_compliance_rule():
    rule = ComplianceRule(
        rule_id="TURNOVER_001",
        name="Minimum Average Turnover",
        description="Bidder must have minimum average annual turnover.",
        rule_type="MIN_AVERAGE_TURNOVER",
        parameters={
            "minimum": 10,
            "currency": "INR",
            "years": ["2023-24", "2024-25", "2025-26"],
        },
        mandatory=True,
    )

    assert rule.rule_id == "TURNOVER_001"
    assert rule.rule_type == "MIN_AVERAGE_TURNOVER"
    assert rule.parameters["minimum"] == 10
    assert rule.mandatory is True


def test_compliance_result():
    result = ComplianceResult(
        rule_id="TURNOVER_001",
        status=ComplianceStatus.PASS,
        message="Average turnover satisfies the requirement.",
        evidence={
            "average": 14.43,
            "required": 10,
        },
        confidence=1.0,
    )

    assert result.rule_id == "TURNOVER_001"
    assert result.status == ComplianceStatus.PASS
    assert result.evidence["average"] == 14.43
    assert result.confidence == 1.0
