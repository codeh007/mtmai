import uuid
from datetime import datetime

from pgvector.sqlalchemy import Vector
from sqlalchemy.dialects.postgresql import TSVECTOR
from sqlmodel import JSON, Column, Field, SQLModel


class SearchIndexBase(SQLModel):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    title: str = Field(...)
    content_type: str = Field(index=True)  # 例如 'post', 'site', 'thread'
    content_id: uuid.UUID = Field(...)
    description: str | None = Field(default=None)  # 显示在列表 item 中的描述栏
    created_at: datetime = Field(default_factory=datetime.now, nullable=False)
    updated_at: datetime = Field(default_factory=datetime.now, nullable=False)


class SearchIndex(SearchIndexBase, table=True):
    __tablename__ = "search_index"
    workspace_id: uuid.UUID | None = Field(default=None, index=True)
    owner_id: uuid.UUID | None = Field(
        foreign_key="user.id", index=True, nullable=False, ondelete="CASCADE"
    )
    is_public: bool = Field(default=True, index=True)
    meta: dict | None = Field(default={}, sa_column=Column(JSON))  # 用于存储额外的元数
    search_vector: str = Field(sa_column=Column(TSVECTOR))
    embedding: list[float] = Field(sa_column=Column(Vector()))
    expired_at: datetime | None = Field(default=None)
    content_summary: str = Field(
        index=True, description="Content summary for full-text search"
    )
    is_deleted: bool = Field(default=False, index=True)


class SearchIndexPublic(SearchIndexBase):
    pass


class SearchIndexResponse(SQLModel):
    data: list[SearchIndexPublic]
    count: int


# Deprecated: Use ListviewRequest instead
class SearchRequest(SQLModel):
    dataType: str | None = None
    q: str | None = None  # 搜索关键词
    limit: int = 100
    skip: int = 0
    # 搜索来自什么应用
    app: str | None = None
