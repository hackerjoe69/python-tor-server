import os
from pydantic import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str = "Realtime Anonymous Server"
    REDIS_HOST: str = os.getenv("REDIS_HOST", "redis")
    REDIS_PORT: int = int(os.getenv("REDIS_PORT", "6379"))
    TOR_HOSTNAME_PATH: str = os.getenv("TOR_HOSTNAME_PATH", "/tor/hostname")

settings = Settings()
