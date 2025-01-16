import uuid
from datetime import datetime

from pgvector.sqlalchemy import Vector
from sqlmodel import JSON, Column, Field, SQLModel


class DocumentIndex(SQLModel, table=True):
    """文档索引表，用途 独立的向量数据库，通过相似查询定位Document

    Args:
        SQLModel (_type_): _description_
        table (bool, optional): _description_. Defaults to True.
    """

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    content_id: str = Field(index=True)  # 关联到 SearchIndex 的 id
    content_type: str
    workspace_id: uuid.UUID | None = Field(default=None, index=True)
    owner_id: uuid.UUID | None = Field(
        foreign_key="user.id", index=True, nullable=False, ondelete="CASCADE"
    )
    meta: dict | None = Field(default={}, sa_column=Column(JSON))  # 用于存储额外的元数
    embedding: list[float] = Field(sa_column=Column(Vector()))
    meta: dict | None = Field(default={}, sa_column=Column(JSON))
    emb_model: str = Field(index=True)
    created_at: datetime = Field(default_factory=datetime.now, nullable=False)
    updated_at: datetime = Field(default_factory=datetime.now, nullable=False)
    is_deleted: bool = Field(default=False, index=True)
    # 类别
    # category: str = Field(default="", index=True)
    # 过期时间
    # expired_at: datetime | None = Field(default=None)
