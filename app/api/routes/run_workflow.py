from fastapi import APIRouter

from app.api.schemes.workflow import WorkflowRequest, WorkflowResponse
from app.graph.workflow import build_initial_state, workflow_app

router = APIRouter()


@router.post("/workflow/run", response_model=WorkflowResponse)
async def run_workflow_endpoint(request: WorkflowRequest):
    initial_state = build_initial_state(request.query)
    result = workflow_app.invoke(initial_state)

    return WorkflowResponse(
        task_type=result["task_type"] or "unknown",
        research_notes=result["research_notes"],
        final_answer=result["final_answer"],
        revision_count=result["revision_count"],
    )