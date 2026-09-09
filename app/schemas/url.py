from datetime import datetime

from pydantic import AnyHttpUrl, BaseModel, Field


class URLCreate(BaseModel):
    original_url: AnyHttpUrl
    custom_alias: str | None = Field(
        default=None,
        min_length=3,
        max_length=50,
        pattern=r"^[a-zA-Z0-9_-]+$",
    )
    expires_at: datetime | None = None


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