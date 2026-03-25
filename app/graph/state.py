from typing import Literal, TypedDict


NextStep = Literal["researcher", "writer", "reviewer", "end"]


class WorkflowState(TypedDict):
    user_query: str
    task_type: str | None
    research_notes: str
    draft_answer: str
    review_feedback: str
    final_answer: str
    revision_count: int
    max_revisions: int
    next_step: NextStep | None