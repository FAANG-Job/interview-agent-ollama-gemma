from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=Path(__file__).resolve().parent / ".env",
        env_file_encoding="utf-8",
    )

    QDRANT_URL: str
    QDRANT_COLLECTION: str
    OLLAMA_URL: str
    OLLAMA_CHAT_MODEL: str
    OLLAMA_EMBED_MODEL: str
    OLLAMA_TIMEOUT_SECONDS: int = Field(gt=0)


settings = Settings()