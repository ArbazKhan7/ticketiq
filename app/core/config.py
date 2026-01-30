from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    # ---- OpenAI ----
    openai_api_key: str = Field(..., env="OPENAI_API_KEY")

    # ---- Twilio ----
    #twilio_account_sid: str = Field(..., env="TWILIO_ACCOUNT_SID")
    #twilio_auth_token: str = Field(..., env="TWILIO_AUTH_TOKEN")
    #twilio_whatsapp_number: str = Field(..., env="TWILIO_WHATSAPP_NUMBER")

    # Meta WhatsApp Cloud API
    meta_access_token: str
    meta_phone_number_id: str
    meta_verify_token: str

    # ---- Database ----
    database_url: str = Field(..., env="DATABASE_URL")

    # ---- Redis (Upstash) ----
    redis_url: str = Field(..., env="REDIS_URL")
    redis_token: str = Field(..., env="REDIS_TOKEN")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra ="ignore"


# Singleton-style access
settings = Settings()
