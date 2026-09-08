from datetime import datetime, timezone
from enum import Enum

from pydantic import BaseModel, Field


class EvidenceSourceType(str, Enum):
    DOCUMENT = "DOCUMENT"
    VERIFICATION_SOURCE = "VERIFICATION_SOURCE"
    RULE_ENGINE = "RULE_ENGINE"


class EvidenceItem(BaseModel):
    """Evidence supporting a compliance decision."""

    source_type: EvidenceSourceType = Field(
        description="Type of source providing the evidence."
    )

    source_name: str = Field(
        description="Human-readable name of the evidence source."
    )

    document_id: str | None = Field(
        default=None,
        description="Identifier of the source document, when applicable."
    )

    field: str | None = Field(
        default=None,
        description="Specific field supported by this evidence."
    )

    value: str | int | float | bool | None = Field(
        default=None,
        description="Value obtained from the evidence source."
    )

    description: str = Field(
        description="Explanation of what this evidence establishes."
    )

    collected_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        description="Time at which the evidence was collected."
    )


class ComplianceEvidence(BaseModel):
    """Complete evidence record for a compliance requirement."""

    rule_id: str = Field(
        description="Compliance rule supported by this evidence."
    )

    items: list[EvidenceItem] = Field(
        default_factory=list,
        description="Evidence items supporting the compliance result."
    )

    summary: str = Field(
        description="Human-readable summary of the available evidence."
    )