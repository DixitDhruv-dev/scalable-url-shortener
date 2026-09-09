from datetime import datetime, timezone

from pydantic import AnyHttpUrl, BaseModel, Field, field_validator


class URLCreate(BaseModel):
    original_url: AnyHttpUrl
    custom_alias: str | None = Field(
        default=None,
        min_length=3,
        max_length=50,
        pattern=r"^[a-zA-Z0-9_-]+$",
    )
    expires_at: datetime | None = None

    @field_validator("expires_at")
    @classmethod
    def validate_expiration(cls, value: datetime | None):
        if value is None:
            return None

        if value.tzinfo is None:
            raise ValueError(
                "expires_at must include timezone information"
            )

        expiration = value.astimezone(timezone.utc)

        if expiration <= datetime.now(timezone.utc):
            raise ValueError(
                "expires_at must be in the future"
            )

        return expiration


class URLResponse(BaseModel):
    id: int
    original_url: str
    short_code: str
    short_url: str
    custom_alias: str | None
    expires_at: datetime | None

    model_config = {
        "from_attributes": True,
    }