"""站点 curd 操作"""

import uuid

from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from mtmai.crud.curd_search import create_site_search_index
from mtmai.models.site import (
    Site,
    SiteCreateRequest,
    SiteHost,
)
# from mtmai.models.task import TaskSchedule


async def get_site_by_id(session: AsyncSession, site_id: uuid.UUID | str):
    if site_id == "testing":
        testing_site = Site(
            id=uuid.uuid4(),
            name="测试站点",
            description="这是一个测试站点",
            # gen_config=TaskSchedule(
            #     site_url="https://www.example.com",
            #     site_topic="AI",
            #     description="AI 相关站点",
            #     keywords="AI, 人工智能, 机器学习",
            # ),
        )
        return testing_site

    if isinstance(site_id, str):
        site_id = uuid.UUID(site_id)
    statement = select(Site).where(Site.id == site_id)
    result = await session.exec(statement)
    return result.one_or_none()


async def get_sites_enabled_automation(session: AsyncSession):
    statement = select(Site).where(Site.enabled_automation == True)  # noqa: E712
    result = await session.exec(statement)
    return result.all()


async def get_site_domain(session: AsyncSession, domain: str):
    """
    TODO: 优化: 可以使用 join select 的方式 一次查询搞定
    """
    statement = select(SiteHost).where(SiteHost.domain == domain)
    site_host = await session.exec(statement)
    site_host = site_host.one_or_none()

    if site_host:
        site = await get_site_by_id(session, site_host.site_id)
        return site
    return None


async def create(
    session: AsyncSession,
    item_in: SiteCreateRequest,
    user_id: uuid.UUID | str | None = None,
):
    site_to_create = Site.model_validate(item_in, update={"owner_id": user_id})
    if user_id:
        site_to_create.owner_id = user_id
    session.add(site_to_create)
    await session.commit()
    await session.refresh(site_to_create)
    await create_site_search_index(session, site_to_create, user_id)
    await session.refresh(site_to_create)
    return site_to_create
