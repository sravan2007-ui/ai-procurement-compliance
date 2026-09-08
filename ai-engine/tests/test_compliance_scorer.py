from app.models.assessment import RiskLevel
from app.models.compliance import (
    ComplianceResult,
    ComplianceStatus,
)
from app.services.compliance_scorer import ComplianceScorer


def test_compliance_scorer_returns_low_risk_when_all_requirements_pass():
    results = [
        ComplianceResult(
            rule_id="RULE_001",
            status=ComplianceStatus.PASS,
            message="Requirement passed.",
            confidence=1.0,
        ),
        ComplianceResult(
            rule_id="RULE_002",
            status=ComplianceStatus.PASS,
            message="Requirement passed.",
            confidence=1.0,
        ),
    ]

    scorer = ComplianceScorer()

    assessment = scorer.assess(results)

    assert assessment.overall_score == 100.0
    assert assessment.risk_level == RiskLevel.LOW
    assert assessment.pass_count == 2
    assert assessment.fail_count == 0


def test_compliance_scorer_returns_high_risk_for_failure():
    results = [
        ComplianceResult(
            rule_id="RULE_001",
            status=ComplianceStatus.PASS,
            message="Requirement passed.",
            confidence=1.0,
        ),
        ComplianceResult(
            rule_id="RULE_002",
            status=ComplianceStatus.FAIL,
            message="Requirement failed.",
            confidence=1.0,
        ),
    ]

    scorer = ComplianceScorer()

    assessment = scorer.assess(results)

    assert assessment.overall_score == 50.0
    assert assessment.risk_level == RiskLevel.HIGH
    assert assessment.fail_count == 1
    assert "failed requirement" in assessment.recommendation


def test_compliance_scorer_returns_medium_risk_for_review():
    results = [
        ComplianceResult(
            rule_id="RULE_001",
            status=ComplianceStatus.PASS,
            message="Requirement passed.",
            confidence=1.0,
        ),
        ComplianceResult(
            rule_id="RULE_002",
            status=ComplianceStatus.REVIEW_REQUIRED,
            message="Manual review required.",
            confidence=0.7,
        ),
    ]

    scorer = ComplianceScorer()

    assessment = scorer.assess(results)

    assert assessment.overall_score == 80.0
    assert assessment.risk_level == RiskLevel.MEDIUM
    assert assessment.review_count == 1


def test_compliance_scorer_returns_high_risk_for_conflict():
    results = [
        ComplianceResult(
            rule_id="RULE_001",
            status=ComplianceStatus.PASS,
            message="Requirement passed.",
            confidence=1.0,
        ),
        ComplianceResult(
            rule_id="RULE_002",
            status=ComplianceStatus.CONFLICT,
            message="Document conflicts with verified source.",
            confidence=1.0,
        ),
    ]

    scorer = ComplianceScorer()

    assessment = scorer.assess(results)

    assert assessment.overall_score == 70.0
    assert assessment.risk_level == RiskLevel.HIGH
    assert assessment.conflict_count == 1
    assert assessment.review_count == 0
    assert "data conflict" in assessment.recommendation

def test_compliance_result_conflict():
    result = ComplianceResult(
        rule_id="CONFLICT_001",
        status=ComplianceStatus.CONFLICT,
        message="Submitted data conflicts with verified data.",
        evidence={
            "document_value": "ABC Pvt Ltd",
            "verified_value": "XYZ Enterprises",
        },
        confidence=1.0,
    )

    assert result.status == ComplianceStatus.CONFLICT