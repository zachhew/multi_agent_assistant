from app.llm.client import get_llm


def route_task(query: str) -> str:
    llm = get_llm()

    prompt = f"""
Classify the request into one label:

comparison
decision
plan
analysis

Return only the label.

Request:
{query}
""".strip()

    response = llm.invoke(prompt)
    task_type = response.content.strip().lower()

    if task_type not in {"comparison", "decision", "plan", "analysis"}:
        return "analysis"

    return task_type