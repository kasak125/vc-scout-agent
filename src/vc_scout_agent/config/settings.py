"""Configuration settings for the VC Scout Agent."""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )
    
    # API Keys
    openrouter_api_key: str
    exa_api_key: str
    
    # Agent Configuration
    model_name: str = "gpt-5-nano"
    temperature: float = 0.7
    openrouter_base_url: str = "https://openrouter.ai/api/v1"
    
    # Search Configuration
    max_search_results: int = 10
    search_days_back: int = 90


settings = Settings()
