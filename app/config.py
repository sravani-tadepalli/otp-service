import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    REDIS_HOST: str = os.getenv("REDIS_HOST", "localhost")
    REDIS_PORT: int = int(os.getenv("REDIS_PORT", 6379))
    REDIS_PASSWORD: str = os.getenv("REDIS_PASSWORD", "")

    OTP_TTL: int = 180  # seconds
    RATE_LIMIT_SECONDS: int = 60  # seconds

settings = Settings()
