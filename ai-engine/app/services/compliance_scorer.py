from app.models.assessment import (
    ComplianceAssessment,
    RiskLevel,
)
from app.models.compliance import (
    ComplianceResult,
    ComplianceStatus,
)


class ComplianceScorer:
    """Aggregate individual compliance results into a bid-level assessment."""

    STATUS_SCORES = {
        ComplianceStatus.PASS: 100.0,
        ComplianceStatus.REVIEW_REQUIRED: 60.0,
        ComplianceStatus.FAIL: 0.0,
    }

    CONFLICT_SCORE = 40.0

    def assess(
        self,
        results: list[ComplianceResult],
    ) -> ComplianceAssessment:

        if not results:
            return ComplianceAssessment(
                overall_score=0.0,
                risk_level=RiskLevel.HIGH,
                results=[],
                pass_count=0,
                fail_count=0,
                review_count=0,
                conflict_count=0,
                recommendation=(
                    "No compliance results are available. "
                    "Procurement Officer review is required."
                ),
            )

        scores = []

        pass_count = 0
        fail_count = 0
        review_count = 0
        conflict_count = 0

        for result in results:
            if result.status == ComplianceStatus.PASS:
                scores.append(self.STATUS_SCORES[ComplianceStatus.PASS])
                pass_count += 1

            elif result.status == ComplianceStatus.FAIL:
                scores.append(self.STATUS_SCORES[ComplianceStatus.FAIL])
                fail_count += 1

            elif result.status == ComplianceStatus.REVIEW_REQUIRED:
                scores.append(
                    self.STATUS_SCORES[ComplianceStatus.REVIEW_REQUIRED]
                )
                review_count += 1

            elif result.status == ComplianceStatus.CONFLICT:
                scores.append(self.CONFLICT_SCORE)
                conflict_count += 1

        overall_score = round(sum(scores) / len(scores), 2)

        risk_level = self._calculate_risk(
            overall_score=overall_score,
            fail_count=fail_count,
            conflict_count=conflict_count,
            review_count=review_count,
        )

        recommendation = self._build_recommendation(
            fail_count=fail_count,
            conflict_count=conflict_count,
            review_count=review_count,
        )

        return ComplianceAssessment(
            overall_score=overall_score,
            risk_level=risk_level,
            results=results,
            pass_count=pass_count,
            fail_count=fail_count,
            review_count=review_count,
            conflict_count=conflict_count,
            recommendation=recommendation,
        )

    @staticmethod
    def _calculate_risk(
        overall_score: float,
        fail_count: int,
        conflict_count: int,
        review_count: int,
    ) -> RiskLevel:

        if fail_count > 0 or conflict_count > 0:
            return RiskLevel.HIGH

        if review_count > 0 or overall_score < 80:
            return RiskLevel.MEDIUM

        return RiskLevel.LOW

    @staticmethod
    def _build_recommendation(
        fail_count: int,
        conflict_count: int,
        review_count: int,
    ) -> str:

        issues = []

        if fail_count:
            issues.append(f"{fail_count} failed requirement(s)")

        if conflict_count:
            issues.append(f"{conflict_count} data conflict(s)")

        if review_count:
            issues.append(f"{review_count} item(s) requiring review")

        if issues:
            return (
                "Procurement Officer review required. "
                + "; ".join(issues)
                + "."
            )

        return (
            "All evaluated compliance requirements passed. "
            "Procurement Officer may proceed with final evaluation."
        )