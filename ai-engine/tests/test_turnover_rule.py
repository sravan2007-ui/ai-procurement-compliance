from app.models.compliance import (
    ComplianceRule,
    ComplianceStatus,
)
from app.models.financial import (
    FinancialDocument,
    FinancialYearTurnover,
)
from app.services.turnover_rule import TurnoverRuleEvaluator


def test_turnover_rule_passes():
    rule = ComplianceRule(
        rule_id="TURNOVER_001",
        name="Minimum Average Turnover",
        description="Minimum average annual turnover is ₹10 crore.",
        rule_type="MIN_AVERAGE_TURNOVER",
        parameters={
            "minimum": 10,
            "years": [
                "2023-24",
                "2024-25",
                "2025-26",
            ],
        },
    )

    financial = FinancialDocument(
        company_name="ABC Technologies Pvt Ltd",
        financial_years=[
            FinancialYearTurnover(
                financial_year="2023-24",
                turnover=12.4,
            ),
            FinancialYearTurnover(
                financial_year="2024-25",
                turnover=14.1,
            ),
            FinancialYearTurnover(
                financial_year="2025-26",
                turnover=16.8,
            ),
        ],
        document_type="CA_TURNOVER_CERTIFICATE",
        confidence=0.95,
    )

    evaluator = TurnoverRuleEvaluator()

    result = evaluator.evaluate(rule, financial)

    assert result.status == ComplianceStatus.PASS
    assert result.evidence["average_turnover"] == 14.43


def test_turnover_rule_fails_when_average_is_below_minimum():
    rule = ComplianceRule(
        rule_id="TURNOVER_002",
        name="Minimum Average Turnover",
        description="Bidder must meet the minimum average turnover.",
        rule_type="MIN_AVERAGE_TURNOVER",
        parameters={
            "minimum": 20,
            "years": ["2023-24", "2024-25", "2025-26"],
        },
    )

    financial_document = FinancialDocument(
        company_name="ABC Pvt Ltd",
        financial_years=[
            FinancialYearTurnover(
                financial_year="2023-24",
                turnover=10,
            ),
            FinancialYearTurnover(
                financial_year="2024-25",
                turnover=12,
            ),
            FinancialYearTurnover(
                financial_year="2025-26",
                turnover=14,
            ),
        ],
        document_type="AUDITED_FINANCIAL_STATEMENT",
        confidence=0.95,
    )

    evaluator = TurnoverRuleEvaluator()

    result = evaluator.evaluate(rule, financial_document)

    assert result.status == ComplianceStatus.FAIL
    assert result.evidence["average_turnover"] == 12.0


def test_turnover_rule_requires_review_when_year_is_missing():
    rule = ComplianceRule(
        rule_id="TURNOVER_003",
        name="Minimum Average Turnover",
        description="Bidder must meet the minimum average turnover.",
        rule_type="MIN_AVERAGE_TURNOVER",
        parameters={
            "minimum": 10,
            "years": ["2023-24", "2024-25", "2025-26"],
        },
    )

    financial_document = FinancialDocument(
        company_name="ABC Pvt Ltd",
        financial_years=[
            FinancialYearTurnover(
                financial_year="2023-24",
                turnover=12,
            ),
            FinancialYearTurnover(
                financial_year="2024-25",
                turnover=14,
            ),
        ],
        document_type="AUDITED_FINANCIAL_STATEMENT",
        confidence=0.95,
    )

    evaluator = TurnoverRuleEvaluator()

    result = evaluator.evaluate(rule, financial_document)

    assert result.status == ComplianceStatus.REVIEW_REQUIRED
    assert result.evidence["missing_year"] == "2025-26"


def test_turnover_rule_requires_review_when_document_is_none():
    rule = ComplianceRule(
        rule_id="TURNOVER_004",
        name="Minimum Average Turnover",
        description="Bidder must meet the minimum average turnover.",
        rule_type="MIN_AVERAGE_TURNOVER",
        parameters={
            "minimum": 10,
            "years": ["2023-24", "2024-25", "2025-26"],
        },
    )

    evaluator = TurnoverRuleEvaluator()
    result = evaluator.evaluate(rule, None)

    assert result.status == ComplianceStatus.REVIEW_REQUIRED
    assert "Financial statement document was not provided." in result.message
    assert result.evidence["minimum_required"] == 10.0


def test_turnover_rule_accepts_dict_input():
    rule = ComplianceRule(
        rule_id="TURNOVER_005",
        name="Minimum Average Turnover",
        description="Bidder must meet the minimum average turnover.",
        rule_type="MIN_AVERAGE_TURNOVER",
        parameters={
            "minimum": 10,
            "years": ["2023-24", "2024-25", "2025-26"],
        },
    )

    financial_dict = {
        "company_name": "ABC Tech",
        "financial_years": [
            {"financial_year": "2023-24", "turnover": 15.0},
            {"financial_year": "2024-25", "turnover": 15.0},
            {"financial_year": "2025-26", "turnover": 15.0},
        ],
        "document_type": "AUDITED_FINANCIAL_STATEMENT",
        "confidence": 0.95,
    }

    evaluator = TurnoverRuleEvaluator()
    result = evaluator.evaluate(rule, financial_dict)

    assert result.status == ComplianceStatus.PASS
    assert result.evidence["average_turnover"] == 15.0