from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


BASE_DIR = Path(__file__).resolve().parent.parent.parent
ENV_FILE = BASE_DIR / ".env"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=ENV_FILE,
        env_file_encoding="utf-8",
    )

    app_name: str = "Multi-Agent Research Assistant"

    llm_base_url: str = "https://openrouter.ai/api/v1"
    llm_api_key: str | None = None
    llm_model_name: str = "openai/gpt-4o-mini"
    llm_temperature: float = 0.1
    llm_max_tokens: int = 1200

    max_revisions: int = 2

    local_knowledge_path: Path = BASE_DIR / "data" / "knowledge" / "knowledge.json"


settings = Settings()