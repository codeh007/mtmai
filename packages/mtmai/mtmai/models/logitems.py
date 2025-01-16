import uuid
from datetime import datetime, timedelta

from pydantic import BaseModel
from sqlmodel import Field, SQLModel


class LogItemBase(SQLModel):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    title: str | None
    level: int = Field(default=3)
    app: str | None
    resource_id: str | None = Field(index=True, description="关联的资源id")
    text: str
    log_type: str | None
    created_at: datetime = Field(default_factory=datetime.now, nullable=False)
    updated_at: datetime = Field(default_factory=datetime.now, nullable=False)
    expire_at: datetime = Field(
        default_factory=lambda: datetime.now() + timedelta(days=7),
        nullable=False,
        description="日志过期时间，默认7天后",
    )


class LogItem(LogItemBase, table=True):
    __tablename__ = "log_item"
    owner_id: uuid.UUID | None = Field(
        # foreign_key="user.id",
        # ondelete="CASCADE",
        index=True,
        nullable=True,
    )
    is_deleted: bool = Field(default=False, index=True)


class LogItemPublic(LogItemBase):
    pass


class LogItemListRequest(BaseModel):
    app: str
    resource_id: str | None = None
    query: str | None
    offset: int | None = 0
    limit: int | None = 100


class LogItemListResponse(BaseModel):
    items: list[LogItemPublic]
    total: int
