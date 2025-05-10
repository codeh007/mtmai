import uuid
from datetime import datetime

from sqlmodel import Field, SQLModel


class DBArtifact(SQLModel, table=True):
    """Represents an artifact stored in the database."""

    __tablename__ = "artifacts"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    created_at: datetime = Field(
        default_factory=datetime.now,
        nullable=False,
    )
    updated_at: datetime = Field(
        default_factory=datetime.now,
        nullable=False,
    )
    type: str | None = Field(default=None)
    version: int | None = Field(default=1)
    session_id: str | None = Field(default=None)
    filename: str | None = Field(default=None)
    app_name: str | None = Field(default=None)
    title: str | None = Field(default=None)
    content: str | None = Field(default=None)
