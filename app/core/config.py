from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    database_url: str
    redis_url: str
    debug: bool = False

    secret_key: str
    algorithm: str

    access_token_expire_minutes: int
    refresh_token_expire_days: int

    minio_endpoint: str
    minio_access_key: str
    minio_secret_key: str
    minio_bucket: str
    minio_secure: bool

    openai_api_key: str

settings = Settings()

from app.core.config import settings

# print("=" * 60)
# print(settings.database_url)
# print("=" * 60)