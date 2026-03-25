import json

from app.llm.client import get_llm


def review_draft(query: str, draft_answer: str) -> dict:
    llm = get_llm()

    prompt = f"""
You are a review agent.

Evaluate the draft answer and decide whether it should be approved or revised.

Return valid JSON only with this schema:
{{
  "decision": "approve" | "revise",
  "feedback": "short feedback"
}}

Rules:
- approve if the answer is structured, relevant, and reasonably complete
- revise if the answer is vague, poorly structured, or missing an important part
- feedback must be short and actionable
- return JSON only

User request:
{query}

Draft answer:
{draft_answer}
""".strip()

    response = llm.invoke(prompt)
    raw = response.content.strip()

    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        return {
            "decision": "revise",
            "feedback": "Make the answer more structured and complete.",
        }

    decision = data.get("decision", "revise")
    feedback = data.get("feedback", "Improve structure and completeness.")

    if decision not in {"approve", "revise"}:
        decision = "revise"

    return {
        "decision": decision,
        "feedback": feedback,
    }