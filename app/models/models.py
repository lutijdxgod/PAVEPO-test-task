from datetime import datetime
from typing import Annotated
from pydantic import EmailStr
from sqlalchemy import (
    TIMESTAMP,
    ForeignKey,
)
from enum import Enum as ENUM
from sqlalchemy.sql import func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base

str_not_nullable_an = Annotated[str, mapped_column(nullable=False)]
str_nullable_an = Annotated[str | None, mapped_column(nullable=True)]
int_not_nullable_an = Annotated[int, mapped_column(nullable=False)]
int_nullable_an = Annotated[int | None, mapped_column(nullable=True)]
datetime_now_not_nullable_an = Annotated[
    datetime,
    mapped_column(TIMESTAMP, nullable=False, server_default=func.now()),
]


class User(Base):
    __tablename__ = "users"

    email: Mapped[str_not_nullable_an]
    name: Mapped[str_nullable_an]
    surname: Mapped[str_nullable_an]

    audio_files = relationship("AudioFile", back_populates="owner")


class AudioFile(Base):
    __tablename__ = "audio_files"

    filename: Mapped[str_not_nullable_an]
    filepath: Mapped[str_not_nullable_an]
    owner_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"), nullable=False
    )
    uploaded_at: Mapped[datetime_now_not_nullable_an]

    owner = relationship("User", back_populates="audio_files")
