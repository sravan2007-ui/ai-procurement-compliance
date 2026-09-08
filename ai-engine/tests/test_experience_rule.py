from app.models.compliance import (
    ComplianceRule,
    ComplianceStatus,
)
from app.models.experience import (
    ExperienceDocument,
    ExperienceProject,
)
from app.services.rules.experience_rule import ExperienceRuleEvaluator


def test_experience_rule_passes_when_requirements_are_met():
    rule = ComplianceRule(
        rule_id="EXP_001",
        name="Relevant Experience",
        description="Bidder must have qualifying refinery projects.",
        rule_type="EXPERIENCE_REQUIREMENT",
        parameters={
            "minimum_projects": 2,
            "minimum_project_value": 5,
            "project_type": "Refinery",
            "experience_years": 5,
            "reference_date": "2026-09-06",
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
                completion_date="2025-03-31",
            ),
            ExperienceProject(
                project_name="Refinery Expansion",
                client_name="Client B",
                project_type="Refinery",
                project_value=6.0,
                completion_date="2025-06-30",
            ),
        ],
        document_type="EXPERIENCE_CERTIFICATE",
        confidence=0.95,
    )

    evaluator = ExperienceRuleEvaluator()

    result = evaluator.evaluate(
        rule,
        experience_document,
    )

    assert result.status == ComplianceStatus.PASS
    assert result.evidence["qualifying_projects"] == 2


def test_experience_rule_fails_when_not_enough_qualifying_projects():
    rule = ComplianceRule(
        rule_id="EXP_002",
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
                project_name="Pipeline Project",
                client_name="Client B",
                project_type="Pipeline",
                project_value=10.0,
            ),
        ],
        document_type="EXPERIENCE_CERTIFICATE",
        confidence=0.95,
    )

    evaluator = ExperienceRuleEvaluator()

    result = evaluator.evaluate(
        rule,
        experience_document,
    )

    assert result.status == ComplianceStatus.FAIL
    assert result.evidence["qualifying_projects"] == 1


def test_experience_rule_requires_review_when_no_projects_exist():
    rule = ComplianceRule(
        rule_id="EXP_003",
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
        projects=[],
        document_type="EXPERIENCE_CERTIFICATE",
        confidence=0.60,
    )

    evaluator = ExperienceRuleEvaluator()

    result = evaluator.evaluate(
        rule,
        experience_document,
    )

    assert result.status == ComplianceStatus.REVIEW_REQUIRED
    assert result.status == ComplianceStatus.REVIEW_REQUIRED

def test_experience_rule_fails_when_projects_are_outside_experience_period():
    rule = ComplianceRule(
        rule_id="EXP_004",
        name="Relevant Experience",
        description="Bidder must have qualifying refinery projects.",
        rule_type="EXPERIENCE_REQUIREMENT",
        parameters={
            "minimum_projects": 2,
            "minimum_project_value": 5,
            "project_type": "Refinery",
            "experience_years": 5,
            "reference_date": "2026-09-06",
        },
    )

    experience_document = ExperienceDocument(
        company_name="ABC Pvt Ltd",
        projects=[
            ExperienceProject(
                project_name="Old Refinery Project",
                client_name="Client A",
                project_type="Refinery",
                project_value=7.5,
                completion_date="2019-03-31",
            ),
            ExperienceProject(
                project_name="Recent Refinery Project",
                client_name="Client B",
                project_type="Refinery",
                project_value=6.0,
                completion_date="2025-06-30",
            ),
        ],
        document_type="EXPERIENCE_CERTIFICATE",
        confidence=0.95,
    )

    evaluator = ExperienceRuleEvaluator()

    result = evaluator.evaluate(
        rule,
        experience_document,
    )

    assert result.status == ComplianceStatus.FAIL
    assert result.evidence["qualifying_projects"] == 1

def test_experience_rule_requires_review_when_completion_date_is_missing():
    rule = ComplianceRule(
        rule_id="EXP_005",
        name="Relevant Experience",
        description="Bidder must have qualifying refinery projects.",
        rule_type="EXPERIENCE_REQUIREMENT",
        parameters={
            "minimum_projects": 2,
            "minimum_project_value": 5,
            "project_type": "Refinery",
            "experience_years": 5,
            "reference_date": "2026-09-06",
        },
    )

    experience_document = ExperienceDocument(
        company_name="ABC Pvt Ltd",
        projects=[
            ExperienceProject(
                project_name="Refinery Project With Missing Date",
                client_name="Client A",
                project_type="Refinery",
                project_value=7.5,
                completion_date=None,
            ),
            ExperienceProject(
                project_name="Recent Refinery Project",
                client_name="Client B",
                project_type="Refinery",
                project_value=6.0,
                completion_date="2025-06-30",
            ),
        ],
        document_type="EXPERIENCE_CERTIFICATE",
        confidence=0.90,
    )

    evaluator = ExperienceRuleEvaluator()

    result = evaluator.evaluate(
        rule,
        experience_document,
    )

    assert result.status == ComplianceStatus.REVIEW_REQUIRED

def test_experience_rule_matches_project_type_with_projects_suffix():
    rule = ComplianceRule(
        rule_id="EXP_006",
        name="Relevant Experience",
        description="Bidder must have qualifying refinery projects.",
        rule_type="EXPERIENCE_REQUIREMENT",
        parameters={
            "minimum_projects": 2,
            "minimum_project_value": 5,
            "project_type": "refinery projects",
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

    evaluator = ExperienceRuleEvaluator()

    result = evaluator.evaluate(
        rule,
        experience_document,
    )

    assert result.status == ComplianceStatus.PASS
    assert result.evidence["qualifying_projects"] == 2