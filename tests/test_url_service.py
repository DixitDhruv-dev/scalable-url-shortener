from unittest.mock import Mock, patch

import pytest

from app.services.url_service import (
    generate_short_code,
    get_original_url,
)


def test_generate_short_code_length():
    code = generate_short_code()

    assert len(code) == 7
    assert code.isalnum()


@patch("app.services.url_service.get_cached_url")
def test_get_original_url_cache_hit(mock_get_cached_url):
    mock_get_cached_url.return_value = "https://google.com/"

    db = Mock()

    result = get_original_url(
        db=db,
        short_code="lNMvS8u",
    )

    assert result == "https://google.com/"
    db.scalar.assert_not_called()


@patch("app.services.url_service.cache_url")
@patch("app.services.url_service.get_cached_url")
def test_get_original_url_cache_miss(
    mock_get_cached_url,
    mock_cache_url,
):
    mock_get_cached_url.return_value = None

    url = Mock()
    url.original_url = "https://github.com/"
    url.short_code = "abc1234"
    url.expires_at = None

    db = Mock()
    db.scalar.return_value = url

    result = get_original_url(
        db=db,
        short_code="abc1234",
    )

    assert result == "https://github.com/"

    db.scalar.assert_called_once()

    mock_cache_url.assert_called_once_with(
        short_code="abc1234",
        original_url="https://github.com/",
        ttl=None,
    )


@patch("app.services.url_service.get_cached_url")
def test_get_original_url_not_found(mock_get_cached_url):
    mock_get_cached_url.return_value = None

    db = Mock()
    db.scalar.return_value = None

    with pytest.raises(ValueError, match="Short URL not found"):
        get_original_url(
            db=db,
            short_code="missing",
        )


@patch("app.services.url_service.get_cached_url")
def test_get_original_url_expired(
    mock_get_cached_url,
):
    mock_get_cached_url.return_value = None

    from datetime import datetime, timedelta, timezone

    url = Mock()
    url.original_url = "https://example.com/"
    url.short_code = "expired"
    url.expires_at = datetime.now(timezone.utc) - timedelta(minutes=5)

    db = Mock()
    db.scalar.return_value = url

    with pytest.raises(
        ValueError,
        match="Short URL has expired",
    ):
        get_original_url(
            db=db,
            short_code="expired",
        )