from app.llm.client import get_llm


def route_task(query: str) -> str:
    llm = get_llm()

    prompt = f"""
You are a routing agent.

Classify the user request into exactly one of these task types:
- comparison
- decision
- plan
- analysis

Rules:
- return only one label
- no explanation
- no punctuation

User request:
{query}
""".strip()

    response = llm.invoke(prompt)
    task_type = response.content.strip().lower()

    allowed = {"comparison", "decision", "plan", "analysis"}
    if task_type not in allowed:
        return "analysis"

    return task_type