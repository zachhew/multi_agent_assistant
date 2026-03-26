def build_structured_notes(raw_text: str) -> str:
    raw_text = raw_text.strip()

    if not raw_text:
        return (
            "1. Key facts\n- No useful facts found.\n\n"
            "2. Options or approaches\n- No clear options identified.\n\n"
            "3. Pros\n- No pros identified.\n\n"
            "4. Cons\n- No cons identified.\n\n"
            "5. Risks\n- No risks identified.\n\n"
            "6. Recommendation factors\n- No recommendation factors identified."
        )

    return (
        "1. Key facts\n"
        f"{raw_text}\n\n"
        "2. Options or approaches\n"
        "- Extract the main options from the material above.\n\n"
        "3. Pros\n"
        "- Extract the main advantages.\n\n"
        "4. Cons\n"
        "- Extract the main disadvantages.\n\n"
        "5. Risks\n"
        "- Extract the main risks or caveats.\n\n"
        "6. Recommendation factors\n"
        "- Identify what should influence the final recommendation."
    )