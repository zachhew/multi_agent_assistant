from pydantic import BaseModel, Field


class WorkflowRequest(BaseModel):
    query: str = Field(..., min_length=5, description="Complex user request for the multi-agent workflow")


class WorkflowResponse(BaseModel):
    task_type: str = Field(..., description="Detected task type")
    research_notes: str = Field(..., description="Collected notes from the research stage")
    final_answer: str = Field(..., description="Final reviewed answer")
    revision_count: int = Field(..., description="How many times the draft was revised")