"""Application configuration loaded from environment variables (PRD §6)."""
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    environment: str = "dev"
    database_url: str = "postgresql+psycopg://visitor:visitor@localhost:5432/visitor"
    secret_key: str = "change-me-in-each-environment"
    allowed_origins: str = "http://localhost:5173"
    aws_region: str = "us-east-1"
    s3_bucket: str = "visitor-dev-files"

    @property
    def origins_list(self) -> list[str]:
        return [o.strip() for o in self.allowed_origins.split(",") if o.strip()]


settings = Settings()
