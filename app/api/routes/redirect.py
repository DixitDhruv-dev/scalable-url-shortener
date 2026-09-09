from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import RedirectResponse
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.cache.redis import get_cached_url, cache_url
from app.db.database import get_db
from app.db.models import URL
# from app.schemas import url


router = APIRouter(tags=["Redirect"])


@router.get("/{short_code}")
def redirect_to_original_url(
    short_code: str,
    db: Session = Depends(get_db),
):
    cached_url = get_cached_url(short_code)

    if cached_url is not None:
        return RedirectResponse(
            url=cached_url,
            status_code=status.HTTP_307_TEMPORARY_REDIRECT,
        )

    url = db.scalar(
        select(URL).where(URL.short_code == short_code)
    )

    if url is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Short URL not found",
        )
    ttl = None

    if url.expires_at is not None:
        now = datetime.now(timezone.utc)

        if url.expires_at <= now:
            raise HTTPException(
                status_code=status.HTTP_410_GONE,
                detail="Short URL has expired",
            )

        ttl = max(1, int((url.expires_at - now).total_seconds()))

    cache_url(
        short_code=url.short_code,
        original_url=url.original_url,
        ttl=ttl,
    )

    return RedirectResponse(
        url=url.original_url,
        status_code=status.HTTP_307_TEMPORARY_REDIRECT,
    )