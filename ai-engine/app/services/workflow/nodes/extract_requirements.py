from app.services.gemini_client import GeminiServiceError
from app.services.tender_requirement_extractor import (
    TenderRequirementExtractor,
)
from app.services.workflow.state import ComplianceGraphState


def extract_requirements(
    state: ComplianceGraphState,
) -> ComplianceGraphState:
    """Extract structured compliance requirements from tender text."""

    if state.get("error"):
        return state

    tender_text = state.get("tender_text", "")
    if not tender_text or not str(tender_text).strip():
        return {
            **state,
            "error": "Tender text is required.",
        }

    try:
        extractor = TenderRequirementExtractor()
        requirement_set = extractor.extract(str(tender_text).strip())

        return {
            **state,
            "requirements": requirement_set.requirements,
            "error": None,
        }

    except GeminiServiceError:
        raise
    except Exception as exc:
        return {
            **state,
            "error": str(exc),
        }
