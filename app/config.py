import os

from pydantic_settings import BaseSettings


def _env_file() -> str:
    env = os.getenv("APP_ENV", "")
    return f".env.{env}" if env else ".env"


class Settings(BaseSettings):
    app_name: str = "MW Global Link API"
    debug: bool = False
    allowed_origins: list[str] = ["http://localhost:3000", "https://*.vercel.app"]
    resend_api_key: str = ""
    supabase_url: str = ""
    supabase_key: str = ""
    ceo_email: str = ""

    model_config = {"env_file": _env_file()}


settings = Settings()
