import redis
from app.config import settings
import logging

logger = logging.getLogger(__name__)

_redis_client = None

def get_redis_client():
    global _redis_client

    if _redis_client:
        return _redis_client

    if not settings.REDIS_HOST:
        logger.warning("REDIS_HOST not set. Redis disabled.")
        return None

    try:
        client = redis.StrictRedis(
            host=settings.REDIS_HOST,
            port=settings.REDIS_PORT,
            password=settings.REDIS_PASSWORD,
            decode_responses=True,
            socket_connect_timeout=2,
            socket_timeout=2,
        )
        client.ping()  # validate connectivity
        _redis_client = client
        logger.info("Connected to Redis")
        return _redis_client

    except Exception as e:
        logger.error(f"Redis unavailable: {e}")
        return None
