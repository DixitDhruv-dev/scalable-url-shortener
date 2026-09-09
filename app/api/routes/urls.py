from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas.url import URLCreate, URLResponse
from app.services.url_service import create_url


router = APIRouter(
    prefix="/urls",
    tags=["URLs"],
)


@router.post(
    "",
    response_model=URLResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_short_url(
    payload: URLCreate,
    db: Session = Depends(get_db),
):
    try:
        url = create_url(
            db=db,
            original_url=str(payload.original_url),
            custom_alias=payload.custom_alias,
            expires_at=payload.expires_at,
        )

    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(exc),
        )

    return URLResponse(
        id=url.id,
        original_url=url.original_url,
        short_code=url.short_code,
        short_url=f"http://localhost:8000/{url.short_code}",
        custom_alias=url.custom_alias,
        expires_at=url.expires_at,
    )