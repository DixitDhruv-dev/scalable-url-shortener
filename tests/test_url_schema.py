from datetime import datetime, timedelta, timezone

import pytest
from pydantic import ValidationError

from app.schemas.url import URLCreate


def test_expiration_must_be_in_future():
    expiration = (
        datetime.now(timezone.utc)
        - timedelta(minutes=1)
    )

    with pytest.raises(
        ValidationError,
        match="expires_at must be in the future",
    ):
        URLCreate(
            original_url="https://example.com",
            expires_at=expiration,
        )


def test_expiration_requires_timezone():
    expiration = datetime.now()

    with pytest.raises(
        ValidationError,
        match="timezone",
    ):
        URLCreate(
            original_url="https://example.com",
            expires_at=expiration,
        )


def test_future_expiration_is_accepted():
    expiration = (
        datetime.now(timezone.utc)
        + timedelta(hours=1)
    )

    payload = URLCreate(
        original_url="https://example.com",
        expires_at=expiration,
    )

    assert payload.expires_at is not None
    assert payload.expires_at.tzinfo is not None