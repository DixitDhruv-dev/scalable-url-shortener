from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import RedirectResponse
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.db.models import URL


router = APIRouter(tags=["Redirect"])


@router.get("/{short_code}")
def redirect_to_original_url(
    short_code: str,
    db: Session = Depends(get_db),
):
    url = db.scalar(
        select(URL).where(URL.short_code == short_code)
    )

    if url is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Short URL not found",
        )

    if url.expires_at is not None:
        now = datetime.now(timezone.utc)

        if url.expires_at <= now:
            raise HTTPException(
                status_code=status.HTTP_410_GONE,
                detail="Short URL has expired",
            )

    return RedirectResponse(
        url=url.original_url,
        status_code=status.HTTP_307_TEMPORARY_REDIRECT,
    )