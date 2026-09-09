from datetime import datetime

from sqlalchemy import DateTime, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.database import Base


class URL(Base):
    __tablename__ = "urls"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True,
    )

    original_url: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    short_code: Mapped[str] = mapped_column(
        String(16),
        unique=True,
        nullable=False,
        index=True,
    )

    custom_alias: Mapped[str | None] = mapped_column(
        String(50),
        unique=True,
        nullable=True,
    )

    expires_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=datetime.utcnow,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )