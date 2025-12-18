  # Configurações (env / parâmetros)
"""
config.py

Centraliza configurações do AvivaHub Demand Analyzer.
Usa pydantic-settings (compatível com Pydantic v2).
"""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Configurações do sistema carregadas via variáveis de ambiente.
    """

    # OpenAI
    OPENAI_API_KEY: str

    # LLM
    LLM_MODEL: str = "gpt-4o-mini"
    LLM_TEMPERATURE: float = 0.2
    LLM_TIMEOUT_SECONDS: int = 20
    LLM_MAX_RETRIES: int = 2

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8"
    )


# Instância única usada no app inteiro
settings = Settings()
