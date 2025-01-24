"""
博客系统api
"""

from fastapi import APIRouter, HTTPException, Query
from sqlmodel import select

from mtmai.crud.curd_blog import get_tags_by_post, update_post
from mtmai.deps import AsyncSessionDep
from mtmai.models.blog import (
    BlogPostDetailResponse,
    BlogPostItem,
    BlogPostListResponse,
    BlogPostUpdateRequest,
    BlogPostUpdateResponse,
    Post,
    PostContent,
)
from mtmai.models.models import Document

router = APIRouter()


@router.get("/posts", response_model=BlogPostListResponse)
async def post_list(
    *,
    db: AsyncSessionDep,
    query: str = Query(default=""),
    offset: int = 0,
    limit: int = Query(default=100, le=100),
):
    if query:
        # 如果有查询字符串，执行向量搜索
        vector_search_query = (
            select(Document.id)
            .order_by(Document.embedding.l2_distance(query))
            .limit(limit * 2)
        )
        relevant_doc_ids = db.exec(vector_search_query).all()

        # 然后使用这些ID来获取完整的博客文章信息
        joined_query = (
            select(Document, Post)
            .join(Post, Document.id == Post.doc_id)
            .where(Document.id.in_(relevant_doc_ids))
            .offset(offset)
            .limit(limit)
        )
    else:
        # 如果没有查询字符串，返回最新的博客文章
        joined_query = (
            select(Post, PostContent)
            .join(PostContent, Post.id == PostContent.post_id)
            .order_by(Post.created_at.desc())
            .offset(offset)
            .limit(limit)
        )
    result = await db.exec(joined_query)
    results = result.all()

    posts = [
        BlogPostItem(
            id=post.id,
            title=post.title or "",
            content=doc.content or "",
            slug=post.slug,
            site_id=post.site_id,
        )
        for post, doc in results
    ]

    return BlogPostListResponse(data=posts, count=len(posts))


# @router.post("/", response_model=BlogPostCreateResponse)
# async def post_create(
#     *,
#     db: AsyncSessionDep,
#     req: BlogPostCreateReq,
# ):
#     return await create_blog_post(session=db, blog_post_create=req)


@router.put("/{post_id}", response_model=BlogPostUpdateResponse)
async def blog_post_update(
    *,
    db: AsyncSessionDep,
    req: BlogPostUpdateRequest,
):
    result = await update_post(session=db, post_update=req)
    return BlogPostUpdateResponse(id=result)


@router.get("/{slug_or_id}", response_model=BlogPostDetailResponse)
async def get_post(
    *,
    slug_or_id: str,
    db: AsyncSessionDep,
):
    """获取 Post 详细完整信息"""
    import uuid

    # Check if slug_or_id is a valid UUID
    try:
        post_id = uuid.UUID(slug_or_id)
        query = select(Post).where(Post.id == post_id)
    except ValueError:
        # If not a valid UUID, treat it as a slug
        query = select(Post).where(Post.slug == slug_or_id)

    a = await db.exec(query)
    blog_post = a.one_or_none()
    if not blog_post:
        raise HTTPException(status_code=404, detail="Post not found")

    # Query the post content
    a = await db.exec(select(PostContent).where(PostContent.post_id == blog_post.id))
    blog_post_content = a.one_or_none()
    if not blog_post_content:
        raise HTTPException(status_code=404, detail="Post content not found")

    tags = await get_tags_by_post(db, blog_post.id)

    return BlogPostDetailResponse(
        id=str(blog_post.id),
        title=blog_post.title,
        content=blog_post_content.content,
        tags=[tag.name for tag in tags],
        created_at=blog_post.created_at,
        updated_at=blog_post.updated_at,
        author=blog_post.author,
    )


# @router.post("/post_test1")
# async def post_test1(
#     *,
#     db: AsyncSessionDep,
# ):
#     result = await flow_article_gen()
#     return result
