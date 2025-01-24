"""博客系统的 curd 操作"""

import random
import string
import uuid

from fastapi import HTTPException
from pydantic import BaseModel
from slugify import slugify
from sqlmodel import Session, delete, func, select
from sqlmodel.ext.asyncio.session import AsyncSession

from mtmai.llm.embedding import embedding_hf
from mtmai.models.blog import (
    BlogPostCreateReq,
    BlogPostUpdateRequest,
    Post,
    PostContent,
    Tag,
    TaggedItem,
)
from mtmai.models.doc import DocumentIndex
from mtmai.models.models import Document
from mtmai.models.search_index import SearchIndex
from mtmai.mtlibs.html.htmlUtils import extract_title_from_html


async def create_blog_post(
    *,
    session: AsyncSession,
    blog_post_create: BlogPostCreateReq,
    user_id: uuid.UUID | str,
) -> Post:
    """
    TODO: 改进1：
        embedding 应该用独立的方式进行，因为调用 embedding_hf 可能失败

    """
    if isinstance(user_id, str):
        user_id = uuid.UUID(user_id)
    input_data = BlogPostCreateReq.model_validate(blog_post_create)
    site_id = input_data.siteId
    if not site_id:
        raise HTTPException(status_code=400, detail="siteId is required")

    if not input_data.content:
        # 前端可以不输入任何直接创建文章
        input_data.content = "<h1>new post</h1><p>post content</p>"
    if not input_data.title:
        input_data.title = extract_title_from_html(input_data.content)
    if not input_data.title:
        input_data.title = "untitled"

    # 处理 slug
    base_slug = slugify(input_data.title)
    slug = base_slug
    while True:
        existing_post = await session.exec(select(Post).where(Post.slug == slug))
        if existing_post.first() is None:
            break
        random_string = "".join(
            random.choices(string.ascii_lowercase + string.digits, k=5)
        )
        slug = f"{base_slug}-{random_string}"
    # Create Post
    new_blog_post = Post(
        title=input_data.title,
        slug=slug,
        site_id=site_id,
        user_id=user_id,
    )

    session.add(new_blog_post)

    # 处理 tags
    if input_data.tags:
        for tag_name in input_data.tags:
            # Check if the tag already exists
            result = await session.exec(
                select(Tag).where(Tag.name == tag_name).where(Tag.site_id == site_id)
            )
            existing_tag = result.first()
            if not existing_tag:
                # If the tag doesn't exist, create a new one
                existing_tag = Tag(name=tag_name, site_id=site_id)
                session.add(existing_tag)

            # Create a TaggedItem to link the post and the tag
            tagged_item = TaggedItem(
                tag_id=existing_tag.id, item_id=new_blog_post.id, item_type="post"
            )
            session.add(tagged_item)

    post_content = PostContent(post_id=new_blog_post.id, content=input_data.content)
    session.add(post_content)

    search_index = SearchIndex(
        content_type="post",
        content_id=new_blog_post.id,
        title=new_blog_post.title,
        meta={
            # "author_id": str(new_blog_post.author_id),
            # "tags": [tag.name for tag in new_blog_post.tags],
        },
        # search_vector=generate_search_vector(post.title, post.content),
        # embedding=generate_embedding(post.title, post.content)
    )
    session.add(search_index)

    await session.commit()
    await session.refresh(new_blog_post)
    return new_blog_post


async def update_post(
    *, session: AsyncSession, post_update: BlogPostUpdateRequest
) -> Post:
    a = await session.exec(select(Post).where(Post.id == post_update.id))
    blog_post = a.one()
    if not blog_post:
        raise HTTPException(status_code=404)
    siteId = (
        blog_post.site_id
    )  # 存储siteId的值，因为后续的 session 操作会改变 blog_post

    title = post_update.title
    blog_post.title = title
    # Update slug if changed
    if post_update.slug and post_update.slug != blog_post.slug:
        existing_post = await session.exec(
            select(Post).where(Post.slug == post_update.slug)
        )
        existing_post = existing_post.first()
        if existing_post:
            raise HTTPException(status_code=400, detail="Slug already exists")
        blog_post.slug = post_update.slug

    await save_post_content(
        session=session, post_id=post_update.id, content=post_update.content
    )

    post_tags = await get_tags_by_post(session, post_update.id)
    existing_tag_names = set(tag.name for tag in post_tags)
    new_tag_names = set(post_update.tags)

    # 删除多余的tags
    await delete_tags_by_post(
        session, post_update.id, existing_tag_names - new_tag_names
    )
    await add_tags_to_posts(
        session, siteId, post_update.id, (new_tag_names - existing_tag_names)
    )

    await session.commit()
    return post_update.id


async def get_post_content(*, session: AsyncSession, post_id: uuid.UUID):
    stmt = select(PostContent).where(PostContent.post_id == post_id)
    post_content = await session.exec(stmt)
    post_content = post_content.one()
    return post_content


async def save_post_content(*, session: AsyncSession, post_id: uuid.UUID, content: str):
    blog_post = await session.exec(
        select(PostContent).where(PostContent.post_id == post_id)
    )
    blog_post = blog_post.one()
    if not blog_post:
        blog_post = PostContent(post_id=post_id, content=content)
        session.add(blog_post)
    else:
        blog_post.content = content

    await session.commit()
    await session.refresh(blog_post)
    return blog_post


async def get_tags_by_post(session: AsyncSession, post_id: uuid.UUID):
    stmt = (
        select(Tag)
        .join(TaggedItem, Tag.id == TaggedItem.tag_id)
        .where(TaggedItem.item_id == post_id)
    )
    result = await session.exec(stmt)
    return result.all()


async def delete_tags_by_post(
    session: AsyncSession, post_id: uuid.UUID, tags_to_remove: set[str]
):
    # First, get the tag IDs for the tags we want to remove
    tag_ids_to_remove = await session.exec(
        select(Tag.id)
        .where(Tag.name.in_(tags_to_remove))
        .where(
            Tag.id.in_(
                select(TaggedItem.tag_id)
                .where(TaggedItem.item_id == post_id)
                .where(TaggedItem.item_type == "post")
            )
        )
    )
    tag_ids_to_remove = tag_ids_to_remove.all()

    # Delete the TaggedItems for this post and the specified tags
    stmt = delete(TaggedItem).where(
        (TaggedItem.item_id == post_id)
        & (TaggedItem.item_type == "post")
        & (TaggedItem.tag_id.in_(tag_ids_to_remove))
    )
    await session.exec(stmt)

    # Commit the changes
    # await session.commit()


async def add_tags_to_posts(
    session: AsyncSession, site_id: uuid.UUID, post_id: uuid.UUID, tags_to_add: set[str]
):
    # First, get or create the tags
    for tag_name in tags_to_add:
        # Check if the tag already exists
        existing_tag = await session.exec(select(Tag).where(Tag.name == tag_name))
        existing_tag = existing_tag.first()

        if existing_tag:
            tag = existing_tag
        else:
            # Create a new tag if it doesn't exist
            tag = Tag(name=tag_name, site_id=site_id)
            session.add(tag)
            await session.flush()  # Flush to get the tag ID

        # Check if the post is already tagged with this tag
        existing_tagged_item = await session.exec(
            select(TaggedItem).where(
                (TaggedItem.item_id == post_id)
                & (TaggedItem.tag_id == tag.id)
                & (TaggedItem.item_type == "post")
            )
        )
        existing_tagged_item = existing_tagged_item.first()

        if not existing_tagged_item:
            # If not, create a new TaggedItem
            tagged_item = TaggedItem(item_id=post_id, tag_id=tag.id, item_type="post")
            session.add(tagged_item)

    # Commit all changes
    # await session.commit()


class DocumentQueryReq(BaseModel):
    query: str
    limit: int = 10
    offset: int = 0


async def document_query(session: Session, req: DocumentQueryReq) -> list[Document]:
    embedding_result = await embedding_hf(inputs=[req.query])
    query = (
        select(Document)
        .join(DocumentIndex, Document.id == DocumentIndex.document_id)
        .order_by(DocumentIndex.embedding.l2_distance(embedding_result[0]))
        .offset(req.offset)
        .limit(req.limit)
    )
    result = session.exec(query).all()
    return result


# async def get_post_detail(*, session: AsyncSession,post_id:str):
#     blog_post = await session.exec(select(Post).where(Post.id == post_id)).one_or_none()
#     if not blog_post:
#         raise HTTPException(status_code=404, detail="Post not found")

#     blog_post_content = await .exec(
#         select(Document).where(Document.id == blog_post.doc_id)
#     ).one_or_none()
#     # if not blog_post_content:
#     #     raise HTTPException(status_code=404, detail="Post content not found")

#     return BlogPostDetailResponse(
#         id=blog_post.id,
#         title=blog_post.title,
#         content=blog_post_content.content,
#         tags=[],  # Assuming tags are not implemented yet
#         author_id=None,  # Assuming author details are not implemented yet
#         author_avatar=None,
#     )


async def get_related_posts(db: AsyncSession, current_post: Post, limit: int = 5):
    """
    获取相关文章(未完成)
    """
    # 获取当前文章的标签
    current_tags = [tag.id for tag in current_post.tags]

    related_posts = (
        await db.query(Post)
        .join(TaggedItem)
        .filter(Post.id != current_post.id)  # 排除当前文章
        .filter(TaggedItem.tag_id.in_(current_tags))  # 匹配标签
        .group_by(Post.id)
        .order_by(func.count(TaggedItem.tag_id).desc())  # 按共享标签数量排序
        .limit(limit)
        .all()
    )
    return related_posts
