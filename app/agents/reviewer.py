import json

from app.llm.client import get_llm


def _criteria_for_task_type(task_type: str | None) -> str:
    mapping = {
        "comparison": """
Checklist for comparison:
1. The answer clearly identifies the compared options.
2. The answer presents trade-offs in a balanced way.
3. The answer explains where each option fits best.
4. The conclusion is balanced and not one-sided too early.
""".strip(),
        "decision": """
Checklist for decision:
1. The answer states the decision context.
2. The answer includes an explicit recommendation.
3. The answer explains why this recommendation is preferred.
4. The answer includes risks or caveats.
5. The answer includes a suggested next step.
""".strip(),
        "plan": """
Checklist for plan:
1. The answer states the objective clearly.
2. The answer provides concrete steps.
3. The answer includes dependencies or prerequisites.
4. The answer includes risks or blockers.
5. The steps are presented in a practical order.
""".strip(),
        "analysis": """
Checklist for analysis:
1. The answer summarizes the situation clearly.
2. The answer includes key observations.
3. The answer provides interpretation, not just facts.
4. The answer explains implications or consequences.
5. The answer ends with a practical takeaway.
""".strip(),
    }
    return mapping.get(task_type or "", mapping["analysis"])


def review_draft(query: str, draft_answer: str, task_type: str | None = None) -> dict:
    llm = get_llm()
    task_criteria = _criteria_for_task_type(task_type)

    prompt = f"""
You are a strict review agent in a multi-agent workflow.

Your job is to review the draft answer against:
1. general quality criteria
2. task-specific criteria

General checklist:
1. The answer directly addresses the user's request.
2. The answer has a clear structure.
3. The answer is practical and not overly generic.
4. The answer is reasonably complete.

Task-specific checklist:
{task_criteria}

Decision rules:
- choose "approve" only if the draft is clearly strong
- choose "revise" if one or more important elements are weak or missing
- be strict but fair

Return valid JSON only with this schema:
{{
  "decision": "approve" | "revise",
  "feedback": "short actionable feedback",
  "missing_elements": ["..."]
}}

Rules:
- feedback must be short, concrete, and actionable
- missing_elements should list weak or missing parts
- return JSON only
- do not include markdown fences

Task type:
{task_type}

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
            "feedback": "Improve task-specific structure and make the answer more complete.",
            "missing_elements": ["task-specific structure", "completeness"],
        }

    decision = data.get("decision", "revise")
    feedback = data.get("feedback", "Improve structure and completeness.")
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