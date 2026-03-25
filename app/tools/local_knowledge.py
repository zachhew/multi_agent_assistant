import json
from pathlib import Path

from app.core.config import settings


def load_knowledge() -> list[dict]:
    path: Path = settings.local_knowledge_path

    if not path.exists():
        return []

    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def local_knowledge_lookup(query: str) -> str:
    knowledge_items = load_knowledge()
    if not knowledge_items:
        return "No local knowledge available."

    query_lower = query.lower()
    matched_items: list[str] = []

    for item in knowledge_items:
        title = item.get("title", "")
        content = item.get("content", "")
        tags = item.get("tags", [])

        searchable_text = " ".join([title, content, " ".join(tags)]).lower()

        if any(word in searchable_text for word in query_lower.split()):
            matched_items.append(
                f"Title: {title}\n"
                f"Tags: {', '.join(tags)}\n"
                f"Content: {content}"
            )

    if not matched_items:
        return "No strongly relevant local knowledge found."

    return "\n\n---\n\n".join(matched_items[:5])