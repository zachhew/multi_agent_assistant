from fastapi import FastAPI

from app.api.routes import run_workflow
from app.core.logging import setup_logging

setup_logging()

app = FastAPI(
    title="Multi-Agent Research Assistant",
    description="LangGraph-based multi-agent workflow for researched and reviewed answers",
    version="0.1.0",
)

app.include_router(run_workflow.router)