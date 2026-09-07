from app.services.compliance_scorer import ComplianceScorer
from app.services.evidence_builder import EvidenceBuilder
from app.services.recommendation.engine import RecommendationEngine
from app.services.workflow.state import ComplianceGraphState


def create_assessment(state: ComplianceGraphState) -> ComplianceGraphState:
    """Create the final bid-level compliance assessment."""

    if state.get("error"):
        return state

    compliance_results = state.get("compliance_results", [])
    bidder_data = state.get("bidder_data", {})
    verification_results = state.get("verification_results", {})
    rules = state.get("rules", [])

    if not compliance_results:
        return {
            **state,
            "assessment": None,
            "error": state.get("error") or "No compliance results are available.",
        }

    try:
        scorer = ComplianceScorer()
        evidence_builder = EvidenceBuilder()
        recommendation_engine = RecommendationEngine()

        assessment = scorer.assess(compliance_results)

        rule_map = {rule.rule_id: rule for rule in rules}
        evidence = []

        for result in compliance_results:
            rule = rule_map.get(result.rule_id)
            data = bidder_data.get(rule.rule_type) if rule else None
            verification = verification_results.get(result.rule_id)

            evidence.append(
                evidence_builder.build(
                    result,
                    data,
                    verification=verification,
                )
            )

        assessment.evidence = evidence

        assessment.recommendation = (
            recommendation_engine.generate(assessment)
        )

        return {
            **state,
            "assessment": assessment,
            "error": None,
        }

    except Exception as exc:
        return {
            **state,
            "error": str(exc),
        }