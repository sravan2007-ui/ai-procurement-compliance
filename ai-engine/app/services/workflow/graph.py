from langgraph.graph import END, START, StateGraph

from app.services.verification.base import VerificationAdapter
from app.services.verification.verification_consistency import (
    VerificationConsistencyChecker,
)
from app.services.workflow.nodes.build_rules import build_rules
from app.services.workflow.nodes.create_assessment import create_assessment
from app.services.workflow.nodes.evaluate_compliance import (
    evaluate_compliance,
)
from app.services.workflow.nodes.extract_requirements import (
    extract_requirements,
)
from app.services.workflow.nodes.verify_bidder import verify_bidder
from app.services.workflow.state import ComplianceGraphState
from app.services.workflow.nodes.retrieve_knowledge import (
    retrieve_knowledge,
)

def build_compliance_graph(
    verification_adapter: VerificationAdapter | None = None,
    consistency_checker: VerificationConsistencyChecker | None = None,
    verification_adapters: dict[str, VerificationAdapter] | None = None,
    rag_service=None,
):
    """Build and compile the AI procurement compliance workflow."""

    graph = StateGraph(ComplianceGraphState)

    graph.add_node(
        "extract_requirements",
        extract_requirements,
    )

    graph.add_node(
        "build_rules",
        build_rules,
    )

    graph.add_node(
    "retrieve_knowledge",
    lambda state: retrieve_knowledge(
        state,
        rag_service=rag_service,
    ),
)

    graph.add_node(
    "verify_bidder",
    lambda state: verify_bidder(
        state,
        verification_adapter=verification_adapter,
        consistency_checker=consistency_checker,
        verification_adapters=verification_adapters,
    ),
)

    graph.add_node(
        "evaluate_compliance",
        evaluate_compliance,
    )

    graph.add_node(
        "create_assessment",
        create_assessment,
    )

    graph.add_edge(
        START,
        "extract_requirements",
    )

    def should_continue(state: ComplianceGraphState) -> str:
        if state.get("error"):
            return "end"
        return "continue"

    graph.add_conditional_edges(
        "extract_requirements",
        should_continue,
        {
            "continue": "build_rules",
            "end": END,
        },
    )

    graph.add_conditional_edges(
        "build_rules",
        should_continue,
        {
            "continue": "retrieve_knowledge",
            "end": END,
        },
    )
    graph.add_conditional_edges(
        "retrieve_knowledge",
        should_continue,
        {
            "continue": "verify_bidder",
            "end": END,
        },
    )
    graph.add_conditional_edges(
        "verify_bidder",
        should_continue,
        {
            "continue": "evaluate_compliance",
            "end": END,
        },
    )

    graph.add_conditional_edges(
        "evaluate_compliance",
        should_continue,
        {
            "continue": "create_assessment",
            "end": END,
        },
    )

    graph.add_edge(
        "create_assessment",
        END,
    )

    return graph.compile()