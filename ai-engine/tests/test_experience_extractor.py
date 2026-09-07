import pymupdf

from app.models.experience import ExperienceDocument
from app.services.experience_extractor import ExperienceExtractor


class FakeGeminiClient:
    def generate_structured(self, prompt, response_model):
        assert response_model is ExperienceDocument
        assert "INR crore" in prompt

        return ExperienceDocument(
            company_name="ABC Technologies Pvt Ltd",
            projects=[
                {
                    "project_name": "Pipeline Installation Project",
                    "client_name": "CPCL",
                    "project_type": "Pipeline",
                    "project_value": 5.0,
                    "completion_date": "2025-03-31",
                }
            ],
            document_type="Experience Certificate",
            raw_text="sample experience certificate",
            confidence=0.95,
            warnings=[],
        )


def test_experience_extractor_returns_structured_data(tmp_path):
    pdf_path = tmp_path / "experience.pdf"

    document = pymupdf.open()
    page = document.new_page()

    page.insert_text(
        (72, 72),
        "ABC Technologies Pvt Ltd\n"
        "Experience Certificate\n"
        "Pipeline Installation Project\n"
        "Client: CPCL\n"
        "Project Value: Rs. 5 crore\n"
        "Completion Date: 31-03-2025",
    )

    document.save(pdf_path)
    document.close()

    extractor = ExperienceExtractor(
        gemini_client=FakeGeminiClient(),
    )

    result = extractor.extract(str(pdf_path))

    assert isinstance(result, ExperienceDocument)
    assert result.company_name == "ABC Technologies Pvt Ltd"
    assert len(result.projects) == 1
    assert result.projects[0].project_name == "Pipeline Installation Project"
    assert result.projects[0].project_value == 5.0
    assert result.projects[0].project_type == "Pipeline"
    assert str(result.projects[0].completion_date) == "2025-03-31"


def test_experience_extractor_rejects_empty_document(tmp_path):
    pdf_path = tmp_path / "empty.pdf"

    document = pymupdf.open()
    document.new_page()
    document.save(pdf_path)
    document.close()

    extractor = ExperienceExtractor(
        gemini_client=FakeGeminiClient(),
    )

    try:
        extractor.extract(str(pdf_path))
    except ValueError as exc:
        assert str(exc) == "No text could be extracted from the document."
    else:
        raise AssertionError("Expected ValueError for empty document")
