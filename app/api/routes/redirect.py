from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.services.url_service import get_original_url


router = APIRouter(tags=["Redirect"])


@router.get("/{short_code}")
def redirect_to_original_url(
    short_code: str,
    db: Session = Depends(get_db),
):
    try:
        original_url = get_original_url(
            db=db,
            short_code=short_code,
        )

    except ValueError as exc:
        message = str(exc)

        if message == "Short URL not found":
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=message,
            )

        if message == "Short URL has expired":
            raise HTTPException(
                status_code=status.HTTP_410_GONE,
                detail=message,
            )

        raise

    return RedirectResponse(
        url=original_url,
        status_code=status.HTTP_307_TEMPORARY_REDIRECT,
    )