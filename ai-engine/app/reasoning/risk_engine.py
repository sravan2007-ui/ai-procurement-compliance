from typing import Any, Dict, List, Optional
from backend.app.schemas.compliance import RiskLevel


class RiskAssessmentResult:
    def __init__(
        self,
        risk_score: float,
        risk_level: RiskLevel,
        reasons: List[str],
        category_breakdown: Dict[str, float],
    ):
        self.risk_score = risk_score
        self.risk_level = risk_level
        self.reasons = reasons
        self.category_breakdown = category_breakdown


class RiskScoringEngine:
    """
    Multi-dimensional AI Risk Scoring Engine.
    Evaluates bid risk across 4 core dimensions:
    1. Statutory Integrity (35% weight)
    2. Financial Viability (25% weight)
    3. Document Authenticity & Completeness (20% weight)
    4. Cross-Document Consistency (20% weight)
    """

    @staticmethod
    def _get(item: Any, key: str, default: Any = "") -> Any:
        if isinstance(item, dict):
            return item.get(key, default)
        return getattr(item, key, default)

    @classmethod
    def evaluate_risk(
        cls,
        statutory_verifications: List[Any],
        compliance_evaluations: List[Any],
        cross_consistency_items: Optional[List[Any]] = None,
        extracted_fields: Optional[Dict[str, str]] = None,
    ) -> RiskAssessmentResult:
        reasons: List[str] = []

        # ----------------------------------------------------------------------
        # Dimension 1: Statutory Integrity (Max 35 points penalty)
        # ----------------------------------------------------------------------
        statutory_penalty = 0.0
        for sv in statutory_verifications:
            source = cls._get(sv, "source_name", cls._get(sv, "source", ""))
            status = cls._get(sv, "status", "")
            conflict_details = cls._get(sv, "conflict_details", cls._get(sv, "message", ""))

            if status in ["CONFLICT_DETECTED", "CONFLICT"]:
                statutory_penalty = 35.0  # Critical statutory breach
                reasons.append(
                    f"CRITICAL STATUTORY CONFLICT: {source} returned conflict. Details: {conflict_details}"
                )
            elif status == "FAILED":
                statutory_penalty = max(statutory_penalty, 25.0)
                reasons.append(f"Statutory check failed for {source}.")

        # ----------------------------------------------------------------------
        # Dimension 2: Financial Viability (Max 25 points penalty)
        # ----------------------------------------------------------------------
        financial_penalty = 0.0
        for ce in compliance_evaluations:
            cat = cls._get(ce, "category", "")
            req_name = cls._get(ce, "requirement_name", "")
            status = cls._get(ce, "status", "")
            evidence = cls._get(ce, "evidence", "")
            score = cls._get(ce, "score", 100.0)

            if cat == "FINANCIAL" or "TURNOVER" in req_name.upper():
                if status == "NON_COMPLIANT":
                    shortfall_ratio = max(0.0, 1.0 - (score / 100.0))
                    financial_penalty = round(25.0 * shortfall_ratio, 1)
                    reasons.append(
                        f"Financial threshold deficit: {evidence} (Compliance score: {score}%)."
                    )

        # ----------------------------------------------------------------------
        # Dimension 3: Document Completeness (Max 20 points penalty)
        # ----------------------------------------------------------------------
        document_penalty = 0.0
        missing_docs = []
        for ce in compliance_evaluations:
            status = cls._get(ce, "status", "")
            evidence = cls._get(ce, "evidence", "") or ""
            mandatory = cls._get(ce, "mandatory", True)
            if "missing" in evidence.lower() and status == "NON_COMPLIANT" and mandatory:
                missing_docs.append(cls._get(ce, "requirement_name", "Mandatory Document"))

        if missing_docs:
            document_penalty = min(20.0, len(missing_docs) * 10.0)
            reasons.append(
                f"Missing {len(missing_docs)} mandatory proof documents: {', '.join(missing_docs)}."
            )

        # ----------------------------------------------------------------------
        # Dimension 4: Cross-Document Consistency (Max 20 points penalty)
        # ----------------------------------------------------------------------
        consistency_penalty = 0.0
        if cross_consistency_items:
            for ci in cross_consistency_items:
                passed = cls._get(ci, "passed", True)
                severity = cls._get(ci, "severity", "LOW")
                details = cls._get(ci, "details", "")
                if not passed:
                    if severity == "CRITICAL":
                        consistency_penalty = max(consistency_penalty, 20.0)
                        reasons.append(f"Cross-document integrity violation: {details}")
                    else:
                        consistency_penalty = min(20.0, consistency_penalty + 10.0)
                        reasons.append(f"Inconsistency detected across documents: {details}")

        # ----------------------------------------------------------------------
        # Overall Risk Score Aggregation
        # ----------------------------------------------------------------------
        total_risk_score = min(
            100.0,
            statutory_penalty + financial_penalty + document_penalty + consistency_penalty,
        )

        if total_risk_score >= 70.0:
            risk_level = RiskLevel.CRITICAL
        elif total_risk_score >= 40.0:
            risk_level = RiskLevel.HIGH
        elif total_risk_score >= 20.0:
            risk_level = RiskLevel.MEDIUM
        else:
            risk_level = RiskLevel.LOW

        if not reasons:
            reasons.append("All statutory verifications and tender compliance checks verified clean.")

        category_breakdown = {
            "statutory_integrity": statutory_penalty,
            "financial_viability": financial_penalty,
            "document_completeness": document_penalty,
            "cross_consistency": consistency_penalty,
        }

        return RiskAssessmentResult(
            risk_score=round(total_risk_score, 1),
            risk_level=risk_level,
            reasons=reasons,
            category_breakdown=category_breakdown,
        )


risk_scoring_engine = RiskScoringEngine()
