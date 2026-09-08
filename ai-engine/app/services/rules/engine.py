from typing import Any
from app.models.compliance import ComplianceResult, ComplianceRule
from app.models.financial import FinancialDocument
from app.services.turnover_rule import TurnoverRuleEvaluator
from app.services.rules.required_document_rule import (
    RequiredDocumentRuleEvaluator,
)
from app.services.rules.gst_status_rule import GSTStatusRuleEvaluator
from app.services.rules.udyam_eligibility_rule import (
    UdyamEligibilityRuleEvaluator,
)
from app.services.rules.experience_rule import ExperienceRuleEvaluator

class ComplianceRuleEngine:
    """Dispatch compliance rules to their corresponding evaluators."""

    def __init__(self) -> None:
        self._evaluators = {
    "MIN_AVERAGE_TURNOVER": TurnoverRuleEvaluator(),
    "REQUIRED_DOCUMENT": RequiredDocumentRuleEvaluator(),
    "GST_STATUS": GSTStatusRuleEvaluator(),
    "UDYAM_ELIGIBILITY": UdyamEligibilityRuleEvaluator(),
    "EXPERIENCE_REQUIREMENT": ExperienceRuleEvaluator(),
}

    def evaluate(
        self,
        rule: ComplianceRule,
        data: Any,
    ) -> ComplianceResult:
        evaluator = self._evaluators.get(rule.rule_type)

        if evaluator is None:
            return ComplianceResult(
                rule_id=rule.rule_id,
                status="REVIEW_REQUIRED",
                message=(
                    f"No evaluator is available for rule type "
                    f"'{rule.rule_type}'."
                ),
                evidence={
                    "rule_type": rule.rule_type,
                },
                confidence=1.0,
            )

        return evaluator.evaluate(rule, data)