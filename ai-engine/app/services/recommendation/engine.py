from app.models.assessment import ComplianceAssessment, RiskLevel


class RecommendationEngine:
    """Generate procurement-officer recommendations from a compliance assessment."""

    def generate(self, assessment: ComplianceAssessment) -> str:
        if not assessment.results:
            return (
                "No compliance requirements were evaluated. "
                "Procurement Officer review is required."
            )

        if assessment.conflict_count > 0:
            return (
                "Procurement Officer review required. "
                "Conflicting information was detected between submitted "
                "documents and/or verified sources. Resolve the conflicts "
                "before final evaluation."
            )

        if assessment.fail_count > 0:
            return (
                "Procurement Officer review required. "
                "One or more mandatory compliance requirements failed. "
                "Review the failed requirements before final evaluation."
            )

        if assessment.review_count > 0:
            return (
                "Procurement Officer review required. "
                "Some requirements could not be conclusively verified. "
                "Review the pending items before final evaluation."
            )

        if assessment.risk_level == RiskLevel.LOW:
            return (
                "All evaluated compliance requirements passed. "
                "Procurement Officer may proceed with final evaluation."
            )

        return (
            "Procurement Officer review required before final evaluation."
        )