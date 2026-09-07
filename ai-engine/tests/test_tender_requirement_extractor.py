from app.models.tender_requirement import TenderRequirementSet
from app.services.tender_requirement_extractor import (
    TenderRequirementExtractor,
)


class FakeGeminiClient:
    def __init__(self, response: TenderRequirementSet) -> None:
        self.response = response
        self.last_prompt = None

    def generate_structured(self, prompt, response_model):
        self.last_prompt = prompt
        assert response_model is TenderRequirementSet
        return self.response


def test_tender_requirement_extractor_returns_structured_requirements():
    expected = TenderRequirementSet(
        requirements=[
            {
                "rule_id": "TURNOVER_001",
                "name": "Minimum Average Annual Turnover",
                "description": (
                    "Bidder must have minimum average annual turnover "
                    "of Rs. 10 crore."
                ),
                "rule_type": "MIN_AVERAGE_TURNOVER",
                "parameters": {
    "minimum": 10,
    "years": [
        "2022-23",
        "2023-24",
        "2024-25",
    ],
},
                "mandatory": True,
                "source_text": (
                    "Average annual turnover shall not be less "
                    "than Rs. 10 crore during the last 3 financial years."
                ),
            }
        ]
    )

    fake_client = FakeGeminiClient(expected)
    extractor = TenderRequirementExtractor(fake_client)

    result = extractor.extract(
        "Average annual turnover shall not be less than Rs. 10 crore "
        "during the last 3 financial years."
    )

    assert len(result.requirements) == 1
    assert result.requirements[0].rule_type == "MIN_AVERAGE_TURNOVER"
    assert (
    result.requirements[0].parameters["minimum"] == 10
)

    assert (
        result.requirements[0].parameters["years"]
        == ["2022-23", "2023-24", "2024-25"]
    )
    assert fake_client.last_prompt is not None


def test_tender_requirement_extractor_rejects_empty_text():
    fake_client = FakeGeminiClient(TenderRequirementSet())
    extractor = TenderRequirementExtractor(fake_client)

    try:
        extractor.extract("   ")
        assert False, "Expected ValueError"
    except ValueError as exc:
        assert str(exc) == "Tender text cannot be empty."


def test_tender_requirement_extractor_builds_compliance_prompt():
    prompt = TenderRequirementExtractor._build_prompt(
        "The bidder must have active GST registration."
    )

    assert "government procurement compliance" in prompt
    assert "GST_STATUS" in prompt
    assert "The bidder must have active GST registration." in prompt
    assert "Do not invent requirements" in prompt
