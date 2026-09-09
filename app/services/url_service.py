import secrets
import string

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