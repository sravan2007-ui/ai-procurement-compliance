from app.models.compliance import ComplianceRule
from app.models.tender_requirement import TenderRequirement


class TenderRuleBuilder:
    """Convert extracted tender requirements into compliance rules."""

    SUPPORTED_RULE_TYPES = {
        "MIN_AVERAGE_TURNOVER",
        "REQUIRED_DOCUMENT",
        "GST_STATUS",
        "UDYAM_ELIGIBILITY",
        "EXPERIENCE_REQUIREMENT",
    }

    def build(self, requirement: TenderRequirement) -> ComplianceRule:
        if requirement.rule_type not in self.SUPPORTED_RULE_TYPES:
            raise ValueError(
                f"Unsupported rule type: {requirement.rule_type}"
            )

        return ComplianceRule(
            rule_id=requirement.rule_id,
            name=requirement.name,
            description=requirement.description,
            rule_type=requirement.rule_type,
            parameters=requirement.parameters,
            mandatory=requirement.mandatory,
        )

    def build_all(
        self,
        requirements: list[TenderRequirement],
    ) -> list[ComplianceRule]:
        return [self.build(requirement) for requirement in requirements]