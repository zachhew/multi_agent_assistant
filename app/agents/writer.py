from app.llm.client import get_llm


def write_draft(
    query: str,
    task_type: str | None,
    research_notes: str,
    review_feedback: str = "",
) -> str:
    llm = get_llm()

    prompt = f"""
You are a writing agent.

Write a structured draft answer for the user.

Requirements:
- be clear and practical
- keep a clean structure
- include a short conclusion or recommendation when appropriate
- incorporate research notes
- if review feedback is provided, revise the draft accordingly

Task type:
{task_type}

User request:
{query}

Research notes:
{research_notes}

Review feedback:
{review_feedback}
""".strip()

    response = llm.invoke(prompt)
    return response.content.strip()