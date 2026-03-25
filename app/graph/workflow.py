from langgraph.graph import END, StateGraph

from app.core.config import settings
from app.graph.nodes import (
    researcher_node,
    reviewer_node,
    route_after_researcher,
    route_after_reviewer,
    route_after_router,
    route_after_writer,
    router_node,
    writer_node,
)
from app.graph.state import WorkflowState


def build_initial_state(user_query: str) -> WorkflowState:
    return WorkflowState(
        user_query=user_query,
        task_type=None,
        research_notes="",
        draft_answer="",
        review_feedback="",
        final_answer="",
        revision_count=0,
        max_revisions=settings.max_revisions,
        next_step=None,
    )


def build_workflow():
    graph = StateGraph(WorkflowState)

    graph.add_node("router", router_node)
    graph.add_node("researcher", researcher_node)
    graph.add_node("writer", writer_node)
    graph.add_node("reviewer", reviewer_node)

    graph.set_entry_point("router")

    graph.add_conditional_edges(
        "router",
        route_after_router,
        {
            "researcher": "researcher",
            "end": END,
        },
    )

    graph.add_conditional_edges(
        "researcher",
        route_after_researcher,
        {
            "writer": "writer",
            "end": END,
        },
    )

    graph.add_conditional_edges(
        "writer",
        route_after_writer,
        {
            "reviewer": "reviewer",
            "end": END,
        },
    )

    graph.add_conditional_edges(
        "reviewer",
        route_after_reviewer,
        {
            "writer": "writer",
            "end": END,
        },
    )

    return graph.compile()


workflow_app = build_workflow()