from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Garage AI"
    app_version: str = "1.0.0"

    database_url: str

    openai_api_key: str = ""

    secret_key: str

    algorithm: str = "HS256"

    access_token_expire_minutes: int = 30

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore"
    )


settings = Settings()
