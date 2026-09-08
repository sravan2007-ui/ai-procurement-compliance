from typing import Any
from app.models.assessment import ComplianceAssessment
from app.models.compliance import ComplianceStatus
from app.models.gst import GSTDocument
from app.services.compliance_scorer import ComplianceScorer
from app.services.evidence_builder import EvidenceBuilder
from app.services.recommendation.engine import RecommendationEngine
from app.services.rules.engine import ComplianceRuleEngine
from app.services.rules.tender_rule_builder import TenderRuleBuilder
from app.services.tender_requirement_extractor import TenderRequirementExtractor
from app.services.verification.base import VerificationAdapter
from app.services.verification.verification_consistency import (
    VerificationConsistencyChecker,
)


class TenderCompliancePipeline:
    """Run tender requirement extraction through final assessment."""

    def __init__(
        self,
        requirement_extractor: TenderRequirementExtractor | None = None,
        rule_builder: TenderRuleBuilder | None = None,
        rule_engine: ComplianceRuleEngine | None = None,
        scorer: ComplianceScorer | None = None,
        recommendation_engine: RecommendationEngine | None = None,
        evidence_builder: EvidenceBuilder | None = None,
        verification_adapter: VerificationAdapter | None = None,
        verification_consistency_checker: (
            VerificationConsistencyChecker | None
        ) = None,
    ) -> None:
        self.requirement_extractor = (
            requirement_extractor or TenderRequirementExtractor()
        )
        self.rule_builder = rule_builder or TenderRuleBuilder()
        self.rule_engine = rule_engine or ComplianceRuleEngine()
        self.scorer = scorer or ComplianceScorer()

        self.verification_adapter = verification_adapter
        self.verification_consistency_checker = (
            verification_consistency_checker
            or VerificationConsistencyChecker()
        )

        self.recommendation_engine = (
            recommendation_engine or RecommendationEngine()
        )
        self.evidence_builder = (
            evidence_builder or EvidenceBuilder()
        )

    def process(
    self,
    tender_text: str,
    bidder_data: dict[str, Any],
    reference_date: str | None = None,
) -> ComplianceAssessment:
        requirements = self.requirement_extractor.extract(tender_text)

        rules = self.rule_builder.build_all(
            requirements.requirements
        )
        if reference_date is not None:
            for rule in rules:
                if rule.rule_type == "EXPERIENCE_REQUIREMENT":
                    rule.parameters["reference_date"] = reference_date

        results = []
        evidence = []

        for rule in rules:
            data = bidder_data.get(rule.rule_type)

            verification = None

            # Verify GST information against an authorized
            # verification source when an adapter is provided.
            if (
                rule.rule_type == "GST_STATUS"
                and isinstance(data, GSTDocument)
                and self.verification_adapter is not None
            ):
                verification = self.verification_adapter.verify(
                    data.gstin
                )

                verification = (
                    self.verification_consistency_checker.compare_gst(
                        data,
                        verification,
                    )
                )

            result = self.rule_engine.evaluate(
                rule,
                data,
            )

            # A conflict from the verification source overrides
            # the normal rule result.
            if verification is not None:
                if verification.status.value == "CONFLICT":
                    result.status = ComplianceStatus.CONFLICT
                    result.message = verification.message
                    result.confidence = verification.confidence

                    result.evidence.update(
                        {
                            "verification_source": verification.source,
                            "verification_status": (
                                verification.status.value
                            ),
                            **verification.verified_data,
                        }
                    )

            results.append(result)

            evidence.append(
                self.evidence_builder.build(
                    result,
                    data,
                    verification=verification,
                )
            )

        # Convert all rule results into the overall assessment.
        assessment = self.scorer.assess(results)

        # Attach evidence for every evaluated requirement.
        assessment.evidence = evidence

        # Generate the final explanation/recommendation.
        assessment.recommendation = (
            self.recommendation_engine.generate(assessment)
        )

        return assessment
