from app.models.experience import (
    ExperienceDocument,
    ExperienceProject,
)


def test_experience_document():
    document = ExperienceDocument(
        company_name="ABC Pvt Ltd",
        projects=[
            ExperienceProject(
                project_name="Refinery Upgrade Project",
                client_name="CPCL",
                project_type="Refinery",
                project_value=7.5,
                completion_date="2025-03-31",
            ),
            ExperienceProject(
                project_name="Pipeline Project",
                client_name="XYZ Ltd",
                project_type="Pipeline",
                project_value=6.0,
                completion_date="2025-06-30",
            ),
        ],
        document_type="EXPERIENCE_CERTIFICATE",
        confidence=0.94,
    )

    assert len(document.projects) == 2
    assert document.projects[0].project_value == 7.5
    assert document.projects[0].project_type == "Refinery"