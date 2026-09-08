from app.models.compliance import ComplianceStatus
from app.services.rules.engine import ComplianceRuleEngine
from app.services.workflow.state import ComplianceGraphState


def evaluate_compliance(
    state: ComplianceGraphState,
) -> ComplianceGraphState:
    """Evaluate all tender rules against bidder data and verification results."""

    if state.get("error"):
        return state

    rules = state.get("rules", [])
    bidder_data = state.get("bidder_data", {})
    verification_results = state.get("verification_results", {})

    if not rules:
        return {
            **state,
            "compliance_results": [],
            "error": "No compliance rules are available.",
        }

    try:
        rule_engine = ComplianceRuleEngine()
        compliance_results = []

        for rule in rules:
            data = bidder_data.get(rule.rule_type)

            result = rule_engine.evaluate(rule, data)

            verification = verification_results.get(rule.rule_id)

            if (
                rule.rule_type == "GST_STATUS"
                and verification is not None
                and verification.status.value == "CONFLICT"
            ):
                result.status = ComplianceStatus.CONFLICT
                result.message = verification.message
                result.confidence = verification.confidence

                result.evidence.update(
                    {
                        "verification_source": verification.source,
                        "verification_status": verification.status.value,
                        **verification.verified_data,
                    }
                )

            compliance_results.append(result)

        return {
            **state,
            "compliance_results": compliance_results,
            "error": None,
        }

    except Exception as exc:
        return {
            **state,
            "error": str(exc),
        }