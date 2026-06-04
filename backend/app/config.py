from pathlib import Path
from pydantic import Field, PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict

# Build an absolute path to the .env at the project root
ENV_PATH = Path(__file__).resolve().parent.parent.parent / ".env"

ALGORITHM = "HS256"

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=ENV_PATH,
        env_file_encoding='utf_8',
        extra="ignore"
    )

    DATABASE_URL: PostgresDsn
    JWT_SECRET: str = Field(min_length=32)
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

settings = Settings()
