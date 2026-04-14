from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "MW Global Link API"
    debug: bool = False
    allowed_origins: list[str] = ["http://localhost:3000", "https://*.vercel.app"]
    resend_api_key: str = ""
    supabase_url: str = ""
    supabase_key: str = ""

    model_config = {"env_file": ".env"}


settings = Settings()
