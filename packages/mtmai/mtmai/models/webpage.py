from sqlmodel import Field, SQLModel


class PageMetaAuthor(SQLModel):
    name: str = Field(default="")
    url: str = Field(default="")


class PageMetaBase(SQLModel):
    title: str | None = Field(default="")
    # 一般是URL的值
    metadataBase: str = Field(default="")
    description: str = Field(default="")
    keywords: list[str] = Field(default=[])
    authors: list[PageMetaAuthor] = Field(default=[])
    creator: str = Field(default="")
    # publisher: str = Field(default="")
    # copyright: str = Field(default="")
    # language: str = Field(default="")
    # image: str = Field(default="")
    # type: str = Field(default="")
    # url: str = Field(default="")
    manifest: str = Field(default="")  # eg. :`${siteConfig.url}/site.webmanifest`,


class PageMetaResponse(PageMetaBase):
    """对应前端页面的 page meta 信息"""

    pass
