"""Configuration management for MBRUS.
Loads settings from environment variables and .env file safely.
"""

from typing import Optional
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application configuration settings."""

    # General
    app_name: str = Field(default="MBRUS", description="Application identity")
    app_env: str = Field(default="development", description="Environment: development, testing, production")
    port: int = Field(default=8000, description="Server port")
    host: str = Field(default="0.0.0.0", description="Server host")
    debug: bool = Field(default=True, description="Debug mode")

    # LLM Provider Configuration
    llm_provider: str = Field(
        default="mock",
        description="LLM provider: 'mock', 'gemini', 'openai'",
    )
    gemini_api_key: Optional[str] = Field(default=None, description="Google Gemini API key")
    openai_api_key: Optional[str] = Field(default=None, description="OpenAI API key")
    default_model: Optional[str] = Field(default=None, description="Custom default model override")

    # Persona & Language
    assistant_name: str = Field(default="MBRUS", description="Assistant persona name")
    default_language: str = Field(default="en-IN", description="Default response language fallback")

    # Voice (Phase 2)
    wake_word: str = Field(default="MBRUS", description="Configurable wake word")
    wake_word_enabled: bool = Field(default=True, description="Whether wake word gating is active")
    stt_provider: str = Field(default="whisper", description="Speech-to-text provider")
    tts_provider: str = Field(default="pyttsx3", description="Text-to-speech provider")

    # Tools & Search (Phase 3)
    weather_api_key: Optional[str] = Field(default=None, description="Weather API key")
    search_api_key: Optional[str] = Field(default=None, description="Web Search API key")

    # RAG & Memory (Phase 4)
    vector_store_dir: str = Field(default="./data/vector_store", description="Directory for vector embeddings")
    memory_store_path: str = Field(default="./data/memory.json", description="File path for long-term memory store")

    # Security & Permissions (Phase 5/6)
    require_confirmation_for_destructive_actions: bool = Field(
        default=True,
        description="Enforce user confirmation before executing consequential/destructive tasks",
    )

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    def get_effective_llm_provider(self) -> str:
        """Determines the active LLM provider.
        If explicitly set to 'gemini' or 'openai', respects that.
        If 'mock' or unset, checks if GEMINI_API_KEY or OPENAI_API_KEY is available.
        """
        if self.llm_provider.lower() == "gemini" and self.gemini_api_key:
            return "gemini"
        if self.llm_provider.lower() == "openai" and self.openai_api_key:
            return "openai"
        if self.gemini_api_key and self.llm_provider.lower() != "mock":
            return "gemini"
        if self.openai_api_key and self.llm_provider.lower() != "mock":
            return "openai"
        return self.llm_provider.lower()


settings = Settings()
