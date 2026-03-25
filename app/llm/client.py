from langchain_openai import ChatOpenAI

from app.core.config import settings

_llm = None


def get_llm() -> ChatOpenAI:
    global _llm

    if not settings.llm_api_key:
        raise ValueError("LLM_API_KEY is not set. Please provide it in the .env file.")

    if _llm is None:
        _llm = ChatOpenAI(
            model=settings.llm_model_name,
            api_key=settings.llm_api_key,
            base_url=settings.llm_base_url,
            temperature=settings.llm_temperature,
            max_tokens=settings.llm_max_tokens,
        )

    return _llm