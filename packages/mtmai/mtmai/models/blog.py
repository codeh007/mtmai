import uuid
from datetime import datetime

from sqlmodel import Field, SQLModel


class TaggedItem(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    tag_id: uuid.UUID = Field(foreign_key="tag.id")
    item_id: uuid.UUID
    item_type: str


class Tag(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    name: str = Field(index=True)
    site_id: uuid.UUID = Field(index=True, foreign_key="site.id", ondelete="CASCADE")

class PostBase(SQLModel):
    title: str | None = Field(default=None, max_length=255)
    slug: str = Field(index=True, unique=True)

    created_at: datetime = Field(default_factory=datetime.now, nullable=False)
    updated_at: datetime = Field(default_factory=datetime.now, nullable=False)
    author: str | None = Field(default=None)
    site_id: uuid.UUID = Field(index=True, foreign_key="site.id", ondelete="CASCADE")
    # content: str | None = Field(default=None)


class Post(PostBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)


class BlogPostItem(PostBase):
    id: uuid.UUID


class BlogPostListResponse(SQLModel):
    data: list[BlogPostItem]
    count: int


class BlogPostCreateReq(SQLModel):
    content: str | None = None
    title: str | None = None
    tags: list[str] = []
    slug: str | None = None
    siteId: uuid.UUID


class BlogPostCreateResponse(SQLModel):
    id: uuid.UUID
    # siteId: uuid.UUID


class BlogPostUpdateRequest(SQLModel):
    id: uuid.UUID
    title: str
    content: str
    slug: str | None = None
    tags: list[str] = []



class BlogPostUpdateResponse(SQLModel):
    id: uuid.UUID



class BlogPostDetailResponse(SQLModel):
    id: uuid.UUID
    title: str
    content: str
    tags: list[str]
    created_at: datetime
    updated_at: datetime
    author: str | None


class PostContent(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    post_id: uuid.UUID = Field(foreign_key="post.id", unique=True, ondelete="CASCADE")
    content: str = Field(default=None)  # Full content


# 练习 tags 与 vedio 的关系
class VideoBase(SQLModel):
    title: str = Field(index=True)
    description: str | None = Field(default=None)
    url: str
    duration: int  # in seconds
    created_at: datetime = Field(default_factory=datetime.now, nullable=False)
    updated_at: datetime = Field(default_factory=datetime.now, nullable=False)
    author: str | None = Field(default=None)


class Video(VideoBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)


class TagItemPublic(SQLModel):
    name: str


class TagListResponse(SQLModel):
    data: list[TagItemPublic]
    count: int
