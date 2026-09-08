from app.models.compliance import (
    ComplianceResult,
    ComplianceRule,
    ComplianceStatus,
)
from app.models.financial import FinancialDocument


class TurnoverRuleEvaluator:
    """Evaluate minimum average annual turnover requirements."""

    def evaluate(
        self,
        rule: ComplianceRule,
        financial_document: FinancialDocument | None,
    ) -> ComplianceResult:
        """Evaluate a minimum average turnover rule."""

        required_minimum = float(rule.parameters.get("minimum", 0))
        required_years = rule.parameters.get("years", [])

        if financial_document is None:
            return ComplianceResult(
                rule_id=rule.rule_id,
                status=ComplianceStatus.REVIEW_REQUIRED,
                message="Financial statement document was not provided.",
                evidence={
                    "required_years": required_years,
                    "minimum_required": required_minimum,
                },
                confidence=1.0,
            )

        if isinstance(financial_document, dict):
            try:
                financial_document = FinancialDocument.model_validate(
                    financial_document
                )
            except Exception:
                return ComplianceResult(
                    rule_id=rule.rule_id,
                    status=ComplianceStatus.REVIEW_REQUIRED,
                    message="Submitted financial statement could not be parsed.",
                    evidence={
                        "required_years": required_years,
                        "minimum_required": required_minimum,
                    },
                    confidence=1.0,
                )

        financial_years = getattr(financial_document, "financial_years", None) or []

        turnovers = []

        for year in required_years:
            matching_year = next(
                (
                    item
                    for item in financial_years
                    if item.financial_year == year
                ),
                None,
            )

            if matching_year is None:
                return ComplianceResult(
                    rule_id=rule.rule_id,
                    status=ComplianceStatus.REVIEW_REQUIRED,
                    message=(
                        f"Turnover information for {year} "
                        "is missing from the submitted document."
                    ),
                    evidence={
                        "missing_year": year,
                        "required_years": required_years,
                    },
                    confidence=getattr(financial_document, "confidence", 1.0),
                )

            turnovers.append(matching_year.turnover)

        if not turnovers:
            return ComplianceResult(
                rule_id=rule.rule_id,
                status=ComplianceStatus.REVIEW_REQUIRED,
                message="No required turnover information was found.",
                evidence={
                    "required_years": required_years,
                },
                confidence=getattr(financial_document, "confidence", 1.0),
            )

        average_turnover = sum(turnovers) / len(turnovers)

        if average_turnover >= required_minimum:
            status = ComplianceStatus.PASS
            message = (
                f"Average turnover is {average_turnover:.2f} crore, "
                f"which meets the minimum requirement of "
                f"{required_minimum:.2f} crore."
            )
        else:
            status = ComplianceStatus.FAIL
            message = (
                f"Average turnover is {average_turnover:.2f} crore, "
                f"which is below the minimum requirement of "
                f"{required_minimum:.2f} crore."
            )

        return ComplianceResult(
            rule_id=rule.rule_id,
            status=status,
            message=message,
            evidence={
                "turnovers": turnovers,
                "required_years": required_years,
                "average_turnover": round(average_turnover, 2),
                "minimum_required": required_minimum,
            },
            confidence=getattr(financial_document, "confidence", 1.0),
        )