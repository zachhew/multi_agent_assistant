from app.llm.client import get_llm
from app.tools.local_knowledge import local_knowledge_lookup


def research_topic(query: str, task_type: str | None) -> str:
    llm = get_llm()
    knowledge = local_knowledge_lookup(query)

    prompt = f"""
You are a research agent.

Your job is to prepare concise research notes for another agent.
Use the provided local knowledge.
Do not write a final answer for the user.
Extract only useful points, trade-offs, and facts.

Task type:
{task_type}

User request:
{query}

Local knowledge:
{knowledge}
""".strip()

    response = llm.invoke(prompt)
    return response.content.strip()