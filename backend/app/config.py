from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    APP_ENV: str = "development"
    APP_URL: str = "http://localhost:3000"
    API_URL: str = "http://localhost:8000"

    DATABASE_URL: str = "postgresql+asyncpg://applypilot:applypilot_dev@localhost:5432/applypilot"
    REDIS_URL: str = "redis://localhost:6379/0"

    CLERK_SECRET_KEY: str = ""
    CLERK_WEBHOOK_SECRET: str = ""

    OPENAI_API_KEY: str = ""
    ANTHROPIC_API_KEY: str = ""
    GOOGLE_AI_API_KEY: str = ""

    PINECONE_API_KEY: str = ""
    PINECONE_INDEX: str = "applypilot-jobs"

    STRIPE_SECRET_KEY: str = ""
    STRIPE_WEBHOOK_SECRET: str = ""

    SENTRY_DSN: str = ""

    # Local JWT settings for fallback auth (used when Clerk is unavailable)
    JWT_SECRET_KEY: str = "replace-me-with-secure-random-string"
    JWT_ALGORITHM: str = "HS256"
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days

    # Use Clerk by default if configured. Set to false to force local auth.
    USE_CLERK: bool = True

    CORS_ORIGINS: list[str] = ["http://localhost:3000"]


settings = Settings()

