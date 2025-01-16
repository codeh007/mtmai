import uuid
from datetime import datetime

from sqlmodel import Field, SQLModel


class TaggedItem(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    tag_id: uuid.UUID = Field(foreign_key="tag.id")
    item_id: uuid.UUID
    item_type: str


class MtkvBase(SQLModel):
    key: str = Field(primary_key=True, index=True)
    value: str
    created_at: datetime = Field(default_factory=datetime.now, nullable=False)
    updated_at: datetime = Field(default_factory=datetime.now, nullable=False)
    expired_at: datetime | None = Field(default=None)


class Mtkv(MtkvBase, table=True):
    pass
