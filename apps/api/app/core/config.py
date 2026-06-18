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

    # Auth / RBAC (VIS-2)
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    refresh_token_expire_minutes: int = 60 * 24 * 7  # 7 days
    password_reset_expire_minutes: int = 30
    # Initial admin seeded by the first migration (override per environment).
    seed_admin_email: str = "admin@visitor.app"
    seed_admin_password: str = "change-me-admin"

    @property
    def origins_list(self) -> list[str]:
        return [o.strip() for o in self.allowed_origins.split(",") if o.strip()]


settings = Settings()
