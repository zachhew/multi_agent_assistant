import json

from app.llm.client import get_llm


def _criteria_for_task_type(task_type: str | None) -> str:
    if task_type == "comparison":
        return (
            "- clearly names the compared options\n"
            "- shows trade-offs fairly\n"
            "- explains where each option fits better\n"
            "- ends with a balanced conclusion"
        )

    if task_type == "decision":
        return (
            "- states the decision clearly\n"
            "- gives an explicit recommendation\n"
            "- explains why this recommendation was chosen\n"
            "- includes risks\n"
            "- includes a next step"
        )

    if task_type == "plan":
        return (
            "- states the goal clearly\n"
            "- includes concrete steps\n"
            "- mentions dependencies\n"
            "- mentions risks or blockers\n"
            "- uses a practical order"
        )

    return (
        "- summarizes the situation clearly\n"
        "- includes observations\n"
        "- interprets them, not just repeats them\n"
        "- explains implications\n"
        "- ends with a practical takeaway"
    )


def review_draft(query: str, draft_answer: str, task_type: str | None = None) -> dict:
    llm = get_llm()
    criteria = _criteria_for_task_type(task_type)

    prompt = f"""
Review the draft.

Approve it only if it is clearly good.
Otherwise ask for revision.

General checks:
- answers the request
- has structure
- is practical
- is complete enough

Task-specific checks:
{criteria}

Return JSON only:
{{
  "decision": "approve" | "revise",
  "feedback": "short actionable feedback",
  "missing_elements": ["..."]
}}

Request:
{query}

Draft:
{draft_answer}
""".strip()

    response = llm.invoke(prompt)
    raw = response.content.strip()

    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        return {
            "decision": "revise",
            "feedback": "Tighten the structure and fill the weak sections.",
            "missing_elements": ["structure", "completeness"],
        }

    decision = data.get("decision", "revise")
    feedback = data.get("feedback", "Tighten the answer and make it more complete.")
    missing_elements = data.get("missing_elements", [])

    if decision not in {"approve", "revise"}:
        decision = "revise"

    if not isinstance(missing_elements, list):
        missing_elements = []

    return {
        "decision": decision,
        "feedback": feedback,
        "missing_elements": missing_elements,
    }