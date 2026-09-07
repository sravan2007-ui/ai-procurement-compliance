from typing import Any, Dict, List, Optional


class ExecutiveSummaryResult:
    def __init__(
        self,
        summary: str,
        recommendation: str,
        recommendation_rationale: str,
    ):
        self.summary = summary
        self.recommendation = recommendation
        self.recommendation_rationale = recommendation_rationale


class ExecutiveSummarizer:
    """Synthesizes technical compliance and forensic verification into executive decision memos."""

    @classmethod
    def generate_summary(
        cls,
        bidder_name: str,
        tender_number: str,
        compliance_score: float,
        risk_score: float,
        risk_level: str,
        risk_reasons: List[str],
        eligibility_status: str,
    ) -> ExecutiveSummaryResult:
        is_clean = risk_level in ["LOW"] and eligibility_status == "QUALIFIED"
        has_critical_conflict = risk_level == "CRITICAL" or any("CRITICAL" in r for r in risk_reasons)

        if has_critical_conflict:
            recommendation = "RECOMMEND_DISQUALIFY"
            recommendation_rationale = (
                f"Critical statutory violation detected. Bidder possesses non-compliant or cancelled statutory credentials "
                f"or active debarment on government registries. Awarding this bid carries high legal and audit liability."
            )
            summary = (
                f"Bidder '{bidder_name}' submitted a bid for Tender {tender_number}. "
                f"Automated verification identified CRITICAL risk factors resulting in an overall compliance score of {compliance_score}% "
                f"and risk index of {risk_score}/100. Key grounds for disqualification: {'; '.join(risk_reasons[:2])}."
            )
        elif eligibility_status == "DISQUALIFIED":
            recommendation = "RECOMMEND_DISQUALIFY"
            recommendation_rationale = (
                f"Bidder failed one or more mandatory tender requirements under the Mandatory Veto Principle. "
                f"Compliance score achieved is {compliance_score}%. Disqualification grounds: {risk_reasons[0] if risk_reasons else 'Mandatory requirement deficit'}."
            )
            summary = (
                f"Bidder '{bidder_name}' failed mandatory technical/financial qualification criteria for Tender {tender_number}. "
                f"Overall compliance score is {compliance_score}%, with a risk level of {risk_level} ({risk_score}/100). "
                f"Primary deficit: {'; '.join(risk_reasons[:2])}."
            )
        elif risk_level == "MEDIUM" or any("missing" in r.lower() for r in risk_reasons):
            recommendation = "RECOMMEND_SEEK_CLARIFICATION"
            recommendation_rationale = (
                "Bidder is technically capable but minor document ambiguities or optional certificate omissions exist. "
                "Procurement officer should request clarification under GeM guideline provisions before final evaluation."
            )
            summary = (
                f"Bidder '{bidder_name}' demonstrates satisfactory general qualification for Tender {tender_number} "
                f"with a compliance score of {compliance_score}%. Risk is evaluated at {risk_level} ({risk_score}/100). "
                f"Clarification is suggested regarding: {'; '.join(risk_reasons[:2])}."
            )
        else:
            recommendation = "RECOMMEND_QUALIFY"
            recommendation_rationale = (
                f"All mandatory statutory credentials (GST, PAN, MCA) and technical specifications have been authoritatively "
                f"verified with zero conflicts. Bidder achieves a perfect compliance score of 100% and a low risk score ({risk_score}/100)."
            )
            summary = (
                f"Bidder '{bidder_name}' is FULLY COMPLIANT with all technical, statutory, and financial requirements for Tender {tender_number}. "
                f"All submitted credentials strictly match authoritative government registers with 100% compliance and LOW risk rating."
            )

        return ExecutiveSummaryResult(
            summary=summary,
            recommendation=recommendation,
            recommendation_rationale=recommendation_rationale,
        )


executive_summarizer = ExecutiveSummarizer()
