import uuid
from datetime import datetime

from sqlmodel import Field, SQLModel


class ProjectBase(SQLModel):
    title: str | None = Field(default=None, max_length=255)
    description: str | None = Field(default=None, max_length=255)
    created_at: datetime = Field(default=datetime.now())
    updated_at: datetime = Field(default=datetime.now())
    enabled: bool | None = Field(default=True)
    owner_id: uuid.UUID | None = Field(
        foreign_key="user.id", index=True, nullable=False, ondelete="CASCADE"
    )
