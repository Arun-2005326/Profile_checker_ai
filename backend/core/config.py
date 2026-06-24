import os
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # GitHub Personal Access Token (optional, increases rate limit)
    GITHUB_TOKEN: str = os.getenv("GITHUB_TOKEN", "")

    # App settings
    APP_NAME: str = "PlacementReady AI"
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"

    # CORS
    ALLOWED_ORIGINS: list = ["*"]

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
