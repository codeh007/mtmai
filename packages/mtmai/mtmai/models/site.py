import uuid
from datetime import datetime
from typing import Literal

from pydantic import BaseModel, HttpUrl
from pydantic import Field as PydanticField
from sqlmodel import JSON, Column, Field, SQLModel


class SitePublishConfig(BaseModel):
    """
    站点发布配置
    """

    publishType: Literal["local", "remove"] = Field(default="local")


class SiteHostBase(SQLModel):
    domain: str = Field(min_length=3, max_length=255)
    is_default: bool = Field(default=False)
    is_https: bool = Field(default=False)
    site_id: uuid.UUID = Field(
        foreign_key="site.id", nullable=False, ondelete="CASCADE"
    )


class SiteHost(SiteHostBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)


class SiteBase(SQLModel):
    """
    用户站点基础配置
    """

    title: str | None = Field(default=None, max_length=255)
    description: str | None = Field(default=None, max_length=255)
    created_at: datetime = Field(default=datetime.now())
    updated_at: datetime = Field(default=datetime.now())
    enabled: bool | None = Field(default=True)
    ########################################################################################
    # 新设计方式：使用第三方站点的方式，例如可以绑定 wordpress 站点
    url: str | None = Field(default=None, max_length=255)
    # 站点的框架，例如 wordpress, typecho, hexo 等
    framework: str | None = Field(default=None, max_length=255)
    # 站点的认证信息，例如 wordpress 的 username, password,
    credential_type: str | None = Field(default=None, max_length=255)
    credentials: str | None = Field(default=None, max_length=255)
    meta: dict | None = Field(default={}, sa_column=Column(JSON))
    enabled_automation: bool | None = Field(default=False)

    # siteGenConfigActiveId: uuid.UUID | None = Field(default=None)
    owner_id: uuid.UUID = Field(
        foreign_key="user.id", index=True, nullable=False, ondelete="CASCADE"
    )


# Database model, database table inferred from class name
class Site(SiteBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    updated_at: datetime = Field(default=datetime.now())
    # site_autos: List["TaskSchedule"] = Relationship(back_populates="site")


class SiteAutoConfig(BaseModel):
    agent_name: str = Field(default="auto_agent", description="agent 名称")
    limit: int = Field(default=10, description="每次生成文章的数量")
    prompt: str = Field(default="", description="生成文章的额外提示词")
    keywords: str | None = Field(default=None, max_length=255, description="关键词")
    sitePublishConfig: SitePublishConfig = Field(default={}, description="站点发布配置")


class SiteCreateRequest(BaseModel):
    url: HttpUrl = PydanticField(
        default=None,
        max_length=255,
        description="网站地址",
        # json_schema_extra={
        #     "label": "网站地址",
        #     "placeholder": "https://example.com",
        #     "icon": "site",
        # },
    )

    class Config:
        json_schema_extra = {
            "title": "站点创建",
        }


class SiteUpdateRequest(SiteBase):
    owner_id: uuid.UUID | None = None


class SiteItemPublic(SiteBase):
    id: uuid.UUID


class ListSiteResponse(SQLModel):
    data: list[SiteItemPublic]
    count: int


class ListSiteHostRequest(SQLModel):
    siteId: uuid.UUID
    q: str | None = Field(default=None, max_length=255)


class SiteHostItemPublic(SiteHostBase):
    id: uuid.UUID


class ListSiteHostsResponse(SQLModel):
    data: list[SiteHostItemPublic]
    count: int


class SiteHostCreateRequest(SiteHostBase):
    site_id: uuid.UUID


class SiteHostCreateResponse(SQLModel):
    id: uuid.UUID


class SiteHostUpdateRequest(SiteHostBase):
    id: uuid.UUID
    host: str = Field(min_length=3, max_length=255)


class SiteHostUpdateResponse(SQLModel):
    id: uuid.UUID


class SiteHostDeleteRequest(SQLModel):
    id: uuid.UUID


class SiteHostDeleteResponse(SQLModel):
    id: uuid.UUID
