def build_decision_frame(task_type: str | None, query: str) -> str:
    if task_type == "decision":
        return f"""
Decision frame:
- Core decision to make
- Available options
- Main trade-offs
- Best recommendation
- Key risks
- Suggested next step

User request:
{query}
""".strip()

    if task_type == "comparison":
        return f"""
Comparison frame:
- Options being compared
- Key dimensions of comparison
- Strengths of each option
- Weaknesses of each option
- Best-fit scenario for each option
- Balanced conclusion

User request:
{query}
""".strip()

    if task_type == "plan":
        return f"""
Planning frame:
- Objective
- Step sequence
- Dependencies
- Risks
- Execution order

User request:
{query}
""".strip()

    return f"""
Analysis frame:
- Situation
- Key observations
- Interpretation
- Implications
- Practical takeaway

User request:
{query}
""".strip()