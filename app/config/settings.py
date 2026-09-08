# from pydantic_settings import BaseSettings, SettingsConfigDict


# class Settings(BaseSettings):

#     app_name: str = "Neatify Backend"
#     app_version: str = "1.0.0"
#     environment: str = "development"
#     secret_key: str

#     supabase_url: str
#     supabase_anon_key: str
#     supabase_service_role_key: str

#     msg91_auth_key: str

#     razorpay_key_id: str
#     razorpay_key_secret: str

#     model_config = SettingsConfigDict(
#         env_file=".env",
#         env_file_encoding="utf-8",
#         extra="ignore",
#     )


# settings = Settings()























# from pydantic_settings import BaseSettings, SettingsConfigDict


# class Settings(BaseSettings):

#     app_name: str = "Neatify Backend"
#     app_version: str = "1.0.0"
#     environment: str = "development"
#     secret_key: str

#     supabase_url: str
#     supabase_anon_key: str
#     supabase_service_role_key: str

#     # =========================
#     # MSG91
#     # =========================
#     msg91_auth_key: str
#     msg91_url: str
#     msg91_integrated_number: str
#     msg91_otp_template_name: str
#     msg91_otp_namespace: str

#     # =========================
#     # RAZORPAY
#     # =========================
#     razorpay_key_id: str
#     razorpay_key_secret: str

#     model_config = SettingsConfigDict(
#         env_file=".env",
#         env_file_encoding="utf-8",
#         extra="ignore",
#     )


# settings = Settings()













from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):

    app_name: str = "Neatify Backend"
    app_version: str = "1.0.0"
    environment: str = "development"
    secret_key: str

    supabase_url: str
    supabase_anon_key: str
    supabase_service_role_key: str

    # =========================
    # MSG91
    # =========================
    # Existing MSG91 / WhatsApp configuration
    msg91_auth_key: str
    msg91_url: str
    msg91_integrated_number: str
    msg91_otp_template_name: str
    msg91_otp_namespace: str

    # New MSG91 Widget configuration
    msg91_verify_access_token_url: str = (
        "https://control.msg91.com/api/v5/widget/verifyAccessToken"
    )

    # =========================
    # RAZORPAY
    # =========================
    razorpay_key_id: str
    razorpay_key_secret: str

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()