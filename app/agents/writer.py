from app.llm.client import get_llm


def _comparison_instructions() -> str:
    return """
Required structure:
1. Task summary
2. Compared options
3. Key trade-offs
4. Best-fit scenarios for each option
5. Balanced conclusion

Focus:
- compare the options side by side
- highlight trade-offs clearly
- avoid turning it into a one-sided memo too early
- the conclusion should still indicate which option is a better fit when appropriate
""".strip()


def _decision_instructions() -> str:
    return """
Required structure:
1. Decision context
2. Main options
3. Recommendation
4. Why this recommendation
5. Risks or caveats
6. Suggested next step

Focus:
- produce a decision-oriented answer
- make the recommendation explicit
- justify the recommendation using the research notes
- keep it practical
""".strip()


def _plan_instructions() -> str:
    return """
Required structure:
1. Objective
2. Proposed steps
3. Dependencies or prerequisites
4. Risks or blockers
5. Recommended execution order

Focus:
- provide an actionable plan
- keep the steps concrete
- make the sequence practical and easy to follow
""".strip()


def _analysis_instructions() -> str:
    return """
Required structure:
1. Situation summary
2. Key observations
3. Interpretation
4. Main implications
5. Practical takeaway

Focus:
- produce an analytical answer
- explain what matters and why
- keep the final takeaway useful and grounded
""".strip()


def _instructions_for_task_type(task_type: str | None) -> str:
    mapping = {
        "comparison": _comparison_instructions(),
        "decision": _decision_instructions(),
        "plan": _plan_instructions(),
        "analysis": _analysis_instructions(),
    }
    return mapping.get(task_type or "", _analysis_instructions())


def write_draft(
    query: str,
    task_type: str | None,
    research_notes: str,
    review_feedback: str = "",
) -> str:
    llm = get_llm()
    task_instructions = _instructions_for_task_type(task_type)

    prompt = f"""
You are a writing agent in a multi-agent workflow.

Your job is to transform internal research notes into a clear final draft for the user.

General rules:
- use only the provided research notes
- do not invent new facts
- write for the user, not for internal workflow
- keep the answer structured and practical
- incorporate review feedback if provided
- make the output match the task type

Task type:
{task_type}

Task-specific writing instructions:
{task_instructions}

User request:
{query}

Research notes:
{research_notes}

Review feedback:
{review_feedback}
""".strip()

    response = llm.invoke(prompt)
    return response.content.strip()