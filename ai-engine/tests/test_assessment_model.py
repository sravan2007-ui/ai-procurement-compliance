from app.models.assessment import (
    ComplianceAssessment,
    RiskLevel,
)


def test_compliance_assessment():
    assessment = ComplianceAssessment(
        overall_score=85.0,
        risk_level=RiskLevel.MEDIUM,
        pass_count=4,
        fail_count=0,
        review_count=1,
        conflict_count=1,
        recommendation="Procurement Officer review required.",
        results=[],
    )

    assert assessment.overall_score == 85.0
    assert assessment.risk_level == RiskLevel.MEDIUM
    assert assessment.pass_count == 4
    assert assessment.review_count == 1