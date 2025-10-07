from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "Calendar Agent"
    credentials_file: Path = Path("credentials.json")
    token_file: Path = Path("token.json")
    scopes: list[str] = ["https://www.googleapis.com/auth/calendar.readonly"]
    log_level: str = "INFO"

@lru_cache
def get_settings():
    return Settings()