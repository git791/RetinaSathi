import os
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    matlab_mode: str = os.getenv("MATLAB_MODE", "mock")
    allowed_origins: str = os.getenv("ALLOWED_ORIGINS", "http://localhost:3000")
    
    # Gemini Explanation Module
    gemini_api_key: str | None = os.getenv("GEMINI_API_KEY")
    gemini_model: str = os.getenv("GEMINI_MODEL", "gemini-2.5-flash-lite")
    gemini_explanation_enabled: bool = os.getenv("GEMINI_EXPLANATION_ENABLED", "true").lower() == "true"
    
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()

