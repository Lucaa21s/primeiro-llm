import os

from app.core.logger import logger

try:
    import redis
except Exception:  # optional dependency in runtime image if not installed yet
    redis = None


REDIS_URL = os.getenv("REDIS_URL", "redis://redis:6379/0")


def get_redis_client():
    if redis is None:
        return None
    return redis.Redis.from_url(REDIS_URL, decode_responses=True)


def redis_ping() -> bool:
    client = get_redis_client()
    if client is None:
        logger.warning("Redis client indisponível (dependência não instalada)")
        return False
    try:
        return bool(client.ping())
    except Exception as error:
        logger.warning("Redis indisponível: %s", error)
        return False
