from app.redis_client import get_redis_client
from app.utils import generate_otp, hash_value
from app.config import settings
from typing import Tuple, Optional
from enum import Enum

class OTPResult(str, Enum):
    SUCCESS = "success"
    RATE_LIMITED = "rate_limited"
    REDIS_UNAVAILABLE = "redis_unavailable"


def create_otp(mobile: str) -> tuple[OTPResult, Optional[str]]:
    client = get_redis_client()
    if not client:
        return OTPResult.REDIS_UNAVAILABLE, None

    rate_key = f"rate:{mobile}"

    if client.exists(rate_key):
        return OTPResult.RATE_LIMITED, None

    otp = generate_otp()
    otp_hash = hash_value(otp)

    client.setex(f"otp:{mobile}", settings.OTP_TTL, otp_hash)
    client.setex(rate_key, settings.RATE_LIMIT_SECONDS, 1)

    print(f"[DEBUG] OTP for {mobile}: {otp}")

    # 🔹 ONLY ADDITION
    return OTPResult.SUCCESS, otp

def verify_otp(mobile: str, otp: str) -> bool:
    client = get_redis_client()
    if not client:
        return False  # Redis required

    stored_hash = client.get(f"otp:{mobile}")
    if not stored_hash:
        return False

    if stored_hash == hash_value(otp):
        client.delete(f"otp:{mobile}")
        return True

    return False
