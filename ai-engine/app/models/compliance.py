from enum import Enum
from typing import Any
from pydantic import BaseModel, Field


class ComplianceStatus(str, Enum):
    PASS = "PASS"
    FAIL = "FAIL"
    REVIEW_REQUIRED = "REVIEW_REQUIRED"
    CONFLICT = "CONFLICT"


class ComplianceRule(BaseModel):
    """A single requirement extracted from a tender."""

    rule_id: str = Field(
        description="Unique identifier for the compliance rule."
    )

    name: str = Field(
        description="Human-readable name of the rule."
    )

    description: str = Field(
        description="Description of what the rule requires."
    )

    rule_type: str = Field(
        description="Type of rule, such as MIN_TURNOVER or REQUIRED_DOCUMENT."
    )

    parameters: dict[str, str | int | float | bool | list[str]] = Field(
        default_factory=dict,
        description="Parameters required to evaluate the rule."
    )

    mandatory: bool = Field(
        default=True,
        description="Whether this requirement is mandatory."
    )


class ComplianceResult(BaseModel):
    """Result produced after evaluating one compliance rule."""

    rule_id: str

    status: ComplianceStatus

    message: str = Field(
        description="Human-readable explanation of the result."
    )

    evidence: dict[str, Any] = Field(
        default_factory=dict,
        description="Evidence used to evaluate the rule."
    )

    confidence: float = Field(
        ge=0.0,
        le=1.0,
        description="Confidence in the evaluation."
    )