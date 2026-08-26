from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):

    app_name: str = "Neatify Backend"
    app_version: str = "1.0.0"
    environment: str = "development"
    secret_key: str

    supabase_url: str
    supabase_anon_key: str
    supabase_service_role_key: str

    msg91_auth_key: str

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()