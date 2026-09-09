import secrets
import string
from datetime import datetime, timezone

from sqlalchemy import select

from app.cache.redis import cache_url, get_cached_url
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.models import URL


SHORT_CODE_ALPHABET = string.ascii_letters + string.digits
SHORT_CODE_LENGTH = 7


def generate_short_code() -> str:
    return "".join(
        secrets.choice(SHORT_CODE_ALPHABET)
        for _ in range(SHORT_CODE_LENGTH)
    )


def create_url(
    db: Session,
    original_url: str,
    custom_alias: str | None = None,
    expires_at=None,
) -> URL:

    if custom_alias:
        existing_url = db.scalar(
            select(URL).where(URL.custom_alias == custom_alias)
        )

        if existing_url:
            raise ValueError("Custom alias already exists")

        short_code = custom_alias

    else:
        while True:
            short_code = generate_short_code()

            existing_url = db.scalar(
                select(URL).where(URL.short_code == short_code)
            )

            if not existing_url:
                break

    url = URL(
        original_url=original_url,
        short_code=short_code,
        custom_alias=custom_alias,
        expires_at=expires_at,
    )

    db.add(url)
    db.commit()
    db.refresh(url)

    return url

def get_original_url(
    db: Session,
    short_code: str,
) -> str:
    cached_url = get_cached_url(short_code)

    if cached_url is not None:
        return cached_url

    url = db.scalar(
        select(URL).where(URL.short_code == short_code)
    )

    if url is None:
        raise ValueError("Short URL not found")

    if url.expires_at is not None:
        now = datetime.now(timezone.utc)

        if url.expires_at <= now:
            raise ValueError("Short URL has expired")

        ttl = int(
            (url.expires_at - now).total_seconds()
        )
    else:
        ttl = None

    cache_url(
        short_code=url.short_code,
        original_url=url.original_url,
        ttl=ttl,
    )

    return url.original_url