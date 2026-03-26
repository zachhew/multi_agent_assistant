from app.llm.client import get_llm
from app.tools.decision_frame_tool import build_decision_frame
from app.tools.local_knowledge import local_knowledge_lookup
from app.tools.structured_note_tool import build_structured_notes


def research_topic(query: str, task_type: str | None) -> str:
    llm = get_llm()
    knowledge = local_knowledge_lookup(query)
    note_scaffold = build_structured_notes(knowledge)
    frame = build_decision_frame(task_type, query)

    prompt = f"""
You are preparing internal notes for another agent.

Do not write the final user-facing answer.
Do not add fluff.
Pull out only working material that will help produce a stronger final response.

Target shape:
- key facts
- options
- pros
- cons
- risks
- recommendation factors

Task type:
{task_type}

Request:
{query}

Framing:
{frame}

Working scaffold:
{note_scaffold}

Local knowledge:
{knowledge}
""".strip()

    response = llm.invoke(prompt)
    return response.content.strip()