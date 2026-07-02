import os

from dotenv import load_dotenv

load_dotenv()


class Settings:
    """Application configuration."""

    OPENROUTER_API_KEY: str | None = os.getenv("OPENROUTER_API_KEY")

    OPENROUTER_MODEL: str = os.getenv(
        "OPENROUTER_MODEL",
        "openai/gpt-4.1-mini",
    )

    OPENROUTER_BASE_URL: str = os.getenv(
        "OPENROUTER_BASE_URL",
        "https://openrouter.ai/api/v1",
    )


settings = Settings()