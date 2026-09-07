from app.services.rag.rag_service import RAGService
from app.services.workflow.state import ComplianceGraphState


def retrieve_knowledge(
    state: ComplianceGraphState,
    rag_service: RAGService | None = None,
) -> ComplianceGraphState:
    """Retrieve relevant procurement knowledge for the tender."""

    service = rag_service or RAGService()

    tender_text = state.get("tender_text", "")

    if not tender_text.strip():
        return {
            **state,
            "error": "Tender text cannot be empty.",
        }

    try:
        retrieved_knowledge = service.retrieve(
            query=tender_text,
            limit=5,
        )
    except Exception as exc:
        return {
            **state,
            "error": str(exc),
        }

    return {
        **state,
        "retrieved_knowledge": retrieved_knowledge,
    }
