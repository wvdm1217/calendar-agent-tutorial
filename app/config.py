from functools import lru_cache
from pathlib import Path
from typing import Optional

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "Calendar Agent"
    credentials_file: Path = Path("credentials.json")
    token_file: Path = Path("token.json")
    scopes: list[str] = ["https://www.googleapis.com/auth/calendar"]
    log_level: str = "INFO"
    auth_port: int = 8888
    google_api_key: Optional[str] = None
    model_provider: str = "google_genai"
    model_name: str = "gemini-2.5-flash"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

@lru_cache
def get_settings():
    return Settings()