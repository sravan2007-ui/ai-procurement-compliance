from app.models.assessment import ComplianceAssessment, RiskLevel
from app.models.compliance import ComplianceResult, ComplianceStatus
from app.services.recommendation.engine import RecommendationEngine


def test_recommendation_for_all_passed_requirements():
    assessment = ComplianceAssessment(
        overall_score=100.0,
        risk_level=RiskLevel.LOW,
        results=[
            ComplianceResult(
                rule_id="RULE_001",
                status=ComplianceStatus.PASS,
                message="Requirement passed.",
                confidence=1.0,
            )
        ],
        pass_count=1,
        fail_count=0,
        review_count=0,
        conflict_count=0,
        recommendation="",
    )

    recommendation = RecommendationEngine().generate(assessment)

    assert "passed" in recommendation
    assert "final evaluation" in recommendation


def test_recommendation_for_failed_requirement():
    assessment = ComplianceAssessment(
        overall_score=0.0,
        risk_level=RiskLevel.HIGH,
        results=[
            ComplianceResult(
                rule_id="RULE_001",
                status=ComplianceStatus.FAIL,
                message="Turnover requirement failed.",
                confidence=1.0,
            )
        ],
        pass_count=0,
        fail_count=1,
        review_count=0,
        conflict_count=0,
        recommendation="",
    )

    recommendation = RecommendationEngine().generate(assessment)

    assert "review required" in recommendation
    assert "failed" in recommendation


def test_recommendation_for_conflict():
    assessment = ComplianceAssessment(
        overall_score=70.0,
        risk_level=RiskLevel.HIGH,
        results=[
            ComplianceResult(
                rule_id="RULE_001",
                status=ComplianceStatus.CONFLICT,
                message="GST data conflict.",
                confidence=1.0,
            )
        ],
        pass_count=0,
        fail_count=0,
        review_count=0,
        conflict_count=1,
        recommendation="",
    )

    recommendation = RecommendationEngine().generate(assessment)

    assert "review required" in recommendation
    assert "Conflicting information" in recommendation

def test_recommendation_for_review_required():
    assessment = ComplianceAssessment(
        overall_score=60.0,
        risk_level=RiskLevel.MEDIUM,
        results=[
            ComplianceResult(
                rule_id="RULE_001",
                status=ComplianceStatus.REVIEW_REQUIRED,
                message="Verification could not be completed.",
                confidence=0.5,
            )
        ],
        pass_count=0,
        fail_count=0,
        review_count=1,
        conflict_count=0,
        recommendation="",
    )

    recommendation = RecommendationEngine().generate(assessment)

    assert "review required" in recommendation
    assert "conclusively verified" in recommendation


def test_recommendation_for_no_results():
    assessment = ComplianceAssessment(
        overall_score=0.0,
        risk_level=RiskLevel.HIGH,
        results=[],
        pass_count=0,
        fail_count=0,
        review_count=0,
        conflict_count=0,
        recommendation="",
    )

    recommendation = RecommendationEngine().generate(assessment)

    assert "No compliance requirements were evaluated" in recommendation