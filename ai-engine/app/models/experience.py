from datetime import date

from pydantic import BaseModel, Field


class ExperienceProject(BaseModel):
    project_name: str = Field(description="Name of the completed project.")
    client_name: str | None = Field(
        default=None,
        description="Client or organization for whom the project was completed.",
    )
    project_type: str | None = Field(
        default=None,
        description="Type or category of the project.",
    )
    project_value: float = Field(
        ge=0,
        description="Value of the project in crore INR.",
    )
    completion_date: date | None = Field(
        default=None,
        description="Project completion date.",
    )


class ExperienceDocument(BaseModel):
    company_name: str = Field(
        description="Name of the bidder or enterprise.",
    )
    projects: list[ExperienceProject] = Field(
        default_factory=list,
        description="Projects cited as relevant experience.",
    )
    document_type: str = Field(
        description="Type of experience document.",
    )
    raw_text: str | None = Field(
        default=None,
        description="Source text used for extraction.",
    )
    confidence: float = Field(
        ge=0.0,
        le=1.0,
        description="AI confidence in the extracted experience information.",
    )
    warnings: list[str] = Field(
        default_factory=list,
        description="Extraction warnings requiring attention.",
    )