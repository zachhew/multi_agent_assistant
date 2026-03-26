from app.llm.client import get_llm


def _instructions_for_task_type(task_type: str | None) -> str:
    if task_type == "comparison":
        return (
            "Write a structured comparison.\n"
            "Include:\n"
            "- short summary\n"
            "- compared options\n"
            "- trade-offs\n"
            "- where each option fits better\n"
            "- balanced conclusion"
        )

    if task_type == "decision":
        return (
            "Write a decision memo.\n"
            "Include:\n"
            "- decision context\n"
            "- options\n"
            "- recommendation\n"
            "- why this recommendation makes sense\n"
            "- risks\n"
            "- next step"
        )

    if task_type == "plan":
        return (
            "Write an execution plan.\n"
            "Include:\n"
            "- objective\n"
            "- concrete steps\n"
            "- dependencies\n"
            "- risks\n"
            "- recommended order"
        )

    return (
        "Write an analytical response.\n"
        "Include:\n"
        "- situation summary\n"
        "- observations\n"
        "- interpretation\n"
        "- implications\n"
        "- practical takeaway"
    )


def write_draft(
    query: str,
    task_type: str | None,
    research_notes: str,
    review_feedback: str = "",
) -> str:
    llm = get_llm()
    instructions = _instructions_for_task_type(task_type)

    prompt = f"""
Turn the internal notes into a clean user-facing answer.

Use only the material provided below.
Do not invent facts.
Keep the answer structured and practical.
If review feedback exists, fix the draft accordingly.

Task type:
{task_type}

Writing instructions:
{instructions}

Request:
{query}

Research notes:
{research_notes}

Review feedback:
{review_feedback}
""".strip()

    response = llm.invoke(prompt)
    return response.content.strip()