from app.services.rules.tender_rule_builder import TenderRuleBuilder
from app.services.workflow.state import ComplianceGraphState


def build_rules(
    state: ComplianceGraphState,
) -> ComplianceGraphState:
    """Convert extracted tender requirements into compliance rules."""

    if state.get("error"):
        return state

    requirements = state.get("requirements", [])

    if not requirements:
        return {
            **state,
            "rules": [],
            "error": "No tender requirements were extracted.",
        }

    try:
        rule_builder = TenderRuleBuilder()
        rules = rule_builder.build_all(requirements)

        reference_date = state.get("reference_date")

        if reference_date is not None:
            for rule in rules:
                if rule.rule_type == "EXPERIENCE_REQUIREMENT":
                    rule.parameters["reference_date"] = reference_date

        return {
            **state,
            "rules": rules,
            "error": None,
        }

    except Exception as exc:
        return {
            **state,
            "error": str(exc),
        }