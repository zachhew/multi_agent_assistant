from app.llm.client import get_llm
from app.tools.decision_frame_tool import build_decision_frame
from app.tools.local_knowledge import local_knowledge_lookup
from app.tools.structured_note_tool import build_structured_notes


def research_topic(query: str, task_type: str | None) -> str:
    llm = get_llm()
    knowledge = local_knowledge_lookup(query)
    structured_base = build_structured_notes(knowledge)
    decision_frame = build_decision_frame(task_type, query)

    prompt = f"""
You are a research agent in a multi-agent workflow.

Your job is to prepare INTERNAL RESEARCH NOTES for another agent.

Important rules:
- do NOT write a final answer for the user
- do NOT write an introduction or conclusion
- do NOT speak directly to the user
- do NOT turn the notes into polished prose
- extract only useful working material for the writing agent

Output format:
1. Key facts
2. Options or approaches
3. Pros
4. Cons
5. Risks
6. Recommendation factors

Task type:
{task_type}

User request:
{query}

Decision frame:
{decision_frame}

Structured base:
{structured_base}

Local knowledge:
{knowledge}
""".strip()

    response = llm.invoke(prompt)
    return response.content.strip()