from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    LLM_MODE: str = "free"  # "free" or "quality"

    GOOGLE_API_KEY: str | None = None
    GROQ_API_KEY: str | None = None
    OPENAI_API_KEY: str | None = None

    GEMINI_MODEL: str = "gemini-2.5-flash"
    GROQ_MODEL: str = "llama-3.3-70b-versatile"

    OPENAI_SQL_MODEL: str = "gpt-4.1-mini"
    OPENAI_FAST_MODEL: str = "gpt-4o-mini"

    class Config:
        env_file = ".env"


settings = Settings()