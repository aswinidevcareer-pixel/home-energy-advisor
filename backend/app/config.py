from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    DATABASE_URL: str = "sqlite:///./home_energy_advisor.db"
    API_V1_PREFIX: str = "/api"
    PROJECT_NAME: str = "Home Energy Advisor API"
    VERSION: str = "1.0.0"
    
    LLM_PROVIDER: str = "ollama"
    
    OLLAMA_BASE_URL: str = "http://localhost:11434"
    OLLAMA_MODEL: str = "llama3.2"

    class Config:
        env_file = ".env"


settings = Settings()
