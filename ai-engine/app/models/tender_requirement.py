from pydantic import BaseModel, Field


class TenderRequirement(BaseModel):
    """A single compliance requirement extracted from a tender."""

    rule_id: str = Field(
        description="Unique identifier for the tender requirement."
    )

    name: str = Field(
        description="Human-readable name of the requirement."
    )

    description: str = Field(
        description="Detailed description of what the tender requires."
    )

    rule_type: str = Field(
        description=(
            "Compliance rule type, such as "
            "MIN_AVERAGE_TURNOVER, REQUIRED_DOCUMENT, "
            "GST_STATUS, UDYAM_ELIGIBILITY, or EXPERIENCE_REQUIREMENT."
        )
    )

    parameters: dict[
        str,
        str | int | float | bool | list[str]
    ] = Field(
        default_factory=dict,
        description="Parameters required to evaluate the requirement."
    )

    mandatory: bool = Field(
        default=True,
        description="Whether this requirement is mandatory."
    )

    source_text: str | None = Field(
        default=None,
        description="Original tender text from which the requirement was extracted."
    )


class TenderRequirementSet(BaseModel):
    """All compliance requirements extracted from a tender."""

    requirements: list[TenderRequirement] = Field(
        default_factory=list,
        description="Structured compliance requirements extracted from the tender."
    )

    warnings: list[str] = Field(
        default_factory=list,
        description="Warnings generated during requirement extraction."
    )