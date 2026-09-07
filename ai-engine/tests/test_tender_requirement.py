from app.models.tender_requirement import (
    TenderRequirement,
    TenderRequirementSet,
)


def test_tender_requirement_creation():
    requirement = TenderRequirement(
        rule_id="TURNOVER_001",
        name="Minimum Average Annual Turnover",
        description="Bidder must have minimum average annual turnover.",
        rule_type="MIN_AVERAGE_TURNOVER",
        parameters={
            "minimum_average_turnover": 100000000,
            "financial_years": 3,
        },
        mandatory=True,
        source_text=(
            "Bidder must have average annual turnover "
            "of at least Rs. 10 crore during the last 3 financial years."
        ),
    )

    assert requirement.rule_id == "TURNOVER_001"
    assert requirement.rule_type == "MIN_AVERAGE_TURNOVER"
    assert requirement.parameters["financial_years"] == 3
    assert requirement.mandatory is True


def test_tender_requirement_defaults():
    requirement = TenderRequirement(
        rule_id="GST_001",
        name="GST Status",
        description="GST registration must be active.",
        rule_type="GST_STATUS",
    )

    assert requirement.parameters == {}
    assert requirement.mandatory is True
    assert requirement.source_text is None


def test_tender_requirement_set():
    requirements = TenderRequirementSet(
        requirements=[
            TenderRequirement(
                rule_id="GST_001",
                name="GST Status",
                description="GST registration must be active.",
                rule_type="GST_STATUS",
                parameters={
                    "required_status": "Active",
                },
            ),
            TenderRequirement(
                rule_id="UDYAM_001",
                name="Udyam Registration",
                description="Bidder must have valid Udyam registration.",
                rule_type="UDYAM_ELIGIBILITY",
                parameters={
                    "allowed_types": ["Micro", "Small", "Medium"],
                },
            ),
        ]
    )

    assert len(requirements.requirements) == 2
    assert requirements.requirements[0].rule_type == "GST_STATUS"
    assert requirements.requirements[1].rule_type == "UDYAM_ELIGIBILITY"
    assert requirements.warnings == []