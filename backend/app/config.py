import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    matlab_mode: str = os.getenv("MATLAB_MODE", "mock")
    allowed_origins: str = os.getenv("ALLOWED_ORIGINS", "http://localhost:3000")
    
    class Config:
        env_file = ".env"

settings = Settings()
