def build_decision_frame(task_type: str | None, query: str) -> str:
    if task_type == "decision":
        return (
            "Think like a short internal decision memo.\n"
            "Cover:\n"
            "- what decision is being made\n"
            "- realistic options\n"
            "- trade-offs\n"
            "- recommendation\n"
            "- risks\n"
            "- immediate next step\n\n"
            f"Request: {query}"
        )

    if task_type == "comparison":
        return (
            "Think like a side-by-side comparison.\n"
            "Cover:\n"
            "- what is being compared\n"
            "- comparison dimensions\n"
            "- strengths of each side\n"
            "- weak points of each side\n"
            "- where each option fits better\n"
            "- balanced final view\n\n"
            f"Request: {query}"
        )

    if task_type == "plan":
        return (
            "Think like an execution plan.\n"
            "Cover:\n"
            "- goal\n"
            "- steps\n"
            "- dependencies\n"
            "- risks\n"
            "- practical order of execution\n\n"
            f"Request: {query}"
        )

    return (
        "Think like an analytical note.\n"
        "Cover:\n"
        "- situation\n"
        "- observations\n"
        "- interpretation\n"
        "- implications\n"
        "- practical takeaway\n\n"
        f"Request: {query}"
    )