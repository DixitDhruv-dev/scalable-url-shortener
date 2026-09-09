from datetime import datetime, timezone

from redis import Redis

from app.core.config import get_settings


settings = get_settings()


redis_client = Redis.from_url(
    settings.redis_url,
    decode_responses=True,
)


def get_cached_url(short_code: str) -> str | None:
    return redis_client.get(f"url:{short_code}")


def cache_url(
    short_code: str,
    original_url: str,
    ttl: int | None = None,
) -> None:
    key = f"url:{short_code}"

    if ttl is not None:
        redis_client.setex(
            key,
            ttl,
            original_url,
        )
    else:
        redis_client.set(
            key,
            original_url,
        )


def delete_cached_url(short_code: str) -> None:
    redis_client.delete(f"url:{short_code}")