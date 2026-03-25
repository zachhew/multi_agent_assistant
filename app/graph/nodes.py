import logging

from app.agents.researcher import research_topic
from app.agents.reviewer import review_draft
from app.agents.router import route_task
from app.agents.writer import write_draft
from app.graph.state import WorkflowState, NextStep

logger = logging.getLogger(__name__)


def router_node(state: WorkflowState) -> WorkflowState:
    logger.info("Router node started")
    task_type = route_task(state["user_query"])
    state["task_type"] = task_type
    state["next_step"] = "researcher"
    logger.info("Router selected task_type=%s", task_type)
    return state


def researcher_node(state: WorkflowState) -> WorkflowState:
    logger.info("Researcher node started")
    notes = research_topic(
        query=state["user_query"],
        task_type=state["task_type"],
    )
    state["research_notes"] = notes
    state["next_step"] = "writer"
    logger.info("Researcher completed")
    return state


def writer_node(state: WorkflowState) -> WorkflowState:
    logger.info("Writer node started | revision_count=%s", state["revision_count"])
    draft = write_draft(
        query=state["user_query"],
        task_type=state["task_type"],
        research_notes=state["research_notes"],
        review_feedback=state["review_feedback"],
    )
    state["draft_answer"] = draft
    state["next_step"] = "reviewer"
    logger.info("Writer completed")
    return state


def reviewer_node(state: WorkflowState) -> WorkflowState:
    logger.info("Reviewer node started")
    review = review_draft(
        query=state["user_query"],
        draft_answer=state["draft_answer"],
    )

    decision = review["decision"]
    feedback = review["feedback"]

    logger.info("Reviewer decision=%s | feedback=%r", decision, feedback)

    if decision == "approve":
        state["final_answer"] = state["draft_answer"]
        state["review_feedback"] = feedback
        state["next_step"] = "end"
        return state

    state["review_feedback"] = feedback
    state["revision_count"] += 1

    if state["revision_count"] >= state["max_revisions"]:
        logger.info("Max revisions reached, accepting last draft")
        state["final_answer"] = state["draft_answer"]
        state["next_step"] = "end"
        return state

    state["next_step"] = "writer"
    return state


def route_after_router(state: WorkflowState) -> NextStep:
    return state["next_step"] or "end"


def route_after_researcher(state: WorkflowState) -> NextStep:
    return state["next_step"] or "end"


def route_after_writer(state: WorkflowState) -> NextStep:
    return state["next_step"] or "end"


def route_after_reviewer(state: WorkflowState) -> NextStep:
    return state["next_step"] or "end"