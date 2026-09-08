from app.models.compliance import (
    ComplianceRule,
    ComplianceStatus,
)
from app.models.financial import (
    FinancialDocument,
    FinancialYearTurnover,
)
from app.services.rules.engine import ComplianceRuleEngine


def test_rule_engine_dispatches_turnover_rule():
    rule = ComplianceRule(
        rule_id="TURNOVER_001",
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
            FinancialYearTurnover(
                financial_year="2025-26",
                turnover=16,
            ),
        ],
        document_type="AUDITED_FINANCIAL_STATEMENT",
        confidence=0.95,
    )

    engine = ComplianceRuleEngine()

    result = engine.evaluate(rule, financial_document)

    assert result.status == ComplianceStatus.PASS
    assert result.rule_id == "TURNOVER_001"

def test_rule_engine_requires_review_for_unknown_rule():
    rule = ComplianceRule(
        rule_id="UNKNOWN_001",
        name="Unknown Rule",
        description="This rule has no evaluator yet.",
        rule_type="UNKNOWN_RULE",
        parameters={},
    )

    engine = ComplianceRuleEngine()

    result = engine.evaluate(rule, {})

    assert result.status == ComplianceStatus.REVIEW_REQUIRED
    assert result.rule_id == "UNKNOWN_001"

def test_rule_engine_dispatches_gst_status_rule():
    from app.models.gst import GSTDocument

    rule = ComplianceRule(
        rule_id="GST_STATUS_001",
        name="Active GST Registration",
        description="Bidder must have an active GST registration.",
        rule_type="GST_STATUS",
        parameters={
            "required_status": "Active",
        },
    )

    gst_document = GSTDocument(
        gstin="29ABCDE1234F1Z5",
        legal_name="ABC Pvt Ltd",
        status="Active",
        confidence=0.98,
    )

    engine = ComplianceRuleEngine()

    result = engine.evaluate(rule, gst_document)

    assert result.status == ComplianceStatus.PASS
    assert result.rule_id == "GST_STATUS_001"

def test_rule_engine_dispatches_udyam_eligibility_rule():
    from app.models.udyam import UdyamDocument

    rule = ComplianceRule(
        rule_id="UDYAM_001",
        name="Udyam Enterprise Eligibility",
        description="Bidder must belong to an allowed enterprise category.",
        rule_type="UDYAM_ELIGIBILITY",
        parameters={
            "allowed_types": ["Small", "Medium"],
        },
    )

    udyam_document = UdyamDocument(
        udyam_number="UDYAM-KA-01-1234567",
        enterprise_name="ABC Pvt Ltd",
        enterprise_type="Small",
        confidence=0.97,
    )

    engine = ComplianceRuleEngine()

    result = engine.evaluate(rule, udyam_document)

    assert result.status == ComplianceStatus.PASS
    assert result.rule_id == "UDYAM_001"

def test_rule_engine_dispatches_experience_rule():
    from app.models.experience import (
        ExperienceDocument,
        ExperienceProject,
    )

    rule = ComplianceRule(
        rule_id="EXP_001",
        name="Relevant Experience",
        description="Bidder must have qualifying refinery projects.",
        rule_type="EXPERIENCE_REQUIREMENT",
        parameters={
            "minimum_projects": 2,
            "minimum_project_value": 5,
            "project_type": "Refinery",
        },
    )

    experience_document = ExperienceDocument(
        company_name="ABC Pvt Ltd",
        projects=[
            ExperienceProject(
                project_name="Refinery Upgrade",
                client_name="Client A",
                project_type="Refinery",
                project_value=7.5,
            ),
            ExperienceProject(
                project_name="Refinery Expansion",
                client_name="Client B",
                project_type="Refinery",
                project_value=6.0,
            ),
        ],
        document_type="EXPERIENCE_CERTIFICATE",
        confidence=0.95,
    )

    engine = ComplianceRuleEngine()

    result = engine.evaluate(
        rule,
        experience_document,
    )

    assert result.status == ComplianceStatus.PASS
    assert result.rule_id == "EXP_001"