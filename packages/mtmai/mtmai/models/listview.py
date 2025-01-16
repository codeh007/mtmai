from datetime import datetime

from pydantic import BaseModel
from sqlmodel import Field


class ListItemAction(BaseModel):
    name: str
    icon: str
    action: str


class ListviewItemPublic(BaseModel):
    id: str
    dataType: str
    title: str
    sub_title: str | None = None
    icon: str | None = None
    description: str | None = None
    updated_at: datetime = Field(default=datetime.now())
    actions: list[ListItemAction] = Field(default=[])
    content_id: str | None = None
    # meta: dict | None = Field(default={}, sa_column=Column(JSON))  # 用于存储额外的元数


class ListviewRequest(BaseModel):
    dataType: str | None = None
    # 变体,   asider | workbench | main
    variables: str | None = None
    q: str | None = None  # 搜索关键词
    limit: int = 100
    skip: int = 0
    # 搜索来自什么应用
    app: str | None = None


class ListVieweRsponse(BaseModel):
    count: int
    items: list[ListviewItemPublic]
