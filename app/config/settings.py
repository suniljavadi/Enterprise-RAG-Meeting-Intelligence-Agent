from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    app_name: str = "Enterprise RAG & Meeting Intelligence Agent"
    database_url: str = "sqlite:///./enterprise_rag.db"
    openai_api_key: str = ""
    openai_base_url: str = ""
    llm_model: str = "gpt-4o-mini"
    embedding_model: str = "local-hash-embedding"
    environment: str = "development"
    log_level: str = "INFO"
    max_upload_mb: int = 25
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

@lru_cache
def get_settings() -> Settings:
    return Settings()
