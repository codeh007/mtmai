import uuid
from typing import Any

from fastapi import APIRouter, HTTPException, Query
from sqlmodel import func, select
import structlog

from mtmai.crud import curd_site
from mtmai.crud.curd_site import get_site_by_id
from mtmai.deps import AsyncSessionDep, CurrentUser, OptionalUserDep
from mtmai.models.blog import Tag, TagListResponse
from mtmai.models.models import (
    Item,
)
from mtmai.models.site import (
    ListSiteHostsResponse,
    ListSiteResponse,
    Site,
    SiteCreateRequest,
    SiteHost,
    SiteHostCreateRequest,
    SiteHostCreateResponse,
    SiteHostDeleteResponse,
    SiteHostUpdateRequest,
    SiteHostUpdateResponse,
    SiteItemPublic,
    SiteUpdateRequest,
)

router = APIRouter()
LOG = structlog.get_logger()


@router.get("/site", response_model=ListSiteResponse)
async def list_sites(session: AsyncSessionDep, current_user: OptionalUserDep) -> Any:
    """
    Retrieve site items.
    """
    count_statement = (
        select(func.count()).select_from(Site).where(Item.owner_id == current_user.id)
    )
    a = await session.exec(count_statement)
    count = a.one()
    statement = (
        select(Site).where(
            Site.owner_id == current_user.id
        )  # .offset(skip).limit(limit)
    )
    r = await session.exec(statement)
    items = r.all()

    return ListSiteResponse(data=items, count=count)


@router.get("/site/{id}", response_model=SiteItemPublic)
async def get_site(session: AsyncSessionDep, current_user: CurrentUser, id: str) -> Any:
    """
    Get site by ID.
    """
    site = await get_site_by_id(session, id)
    if site is None or site.owner_id != current_user.id:
        raise HTTPException(status_code=404, detail="not found")
    return site


@router.post("/site/create", response_model=SiteItemPublic)
async def site_create(
    *,
    session: AsyncSessionDep,
    current_user: CurrentUser,
    item_in: SiteCreateRequest,
) -> Any:
    return await curd_site.create(
        session, SiteCreateRequest.model_validate(item_in), user_id=current_user.id
    )


@router.put("/site/update/{id}", response_model=SiteItemPublic)
async def site_update(
    *,
    session: AsyncSessionDep,
    current_user: CurrentUser,
    id: str,
    item_in: SiteUpdateRequest,
) -> Any:
    """
    Update an item.
    """
    site = await get_site_by_id(session, id)
    if site is None or site.owner_id != current_user.id:
        raise HTTPException(status_code=404, detail="Item not found")

    update_dict = item_in.model_dump(exclude_unset=True)
    site.sqlmodel_update(update_dict)
    session.add(site)
    await session.commit()
    await session.refresh(site)
    return site


@router.get("/hosts", response_model=ListSiteHostsResponse)
async def list_site_hosts(
    session: AsyncSessionDep,
    current_user: OptionalUserDep,
    q: str | None = None,
    siteId: uuid.UUID | None = None,
    skip: int = 0,
    limit: int = 100,
) -> Any:
    """
    Retrieve site hosts.
    """
    count_statement = (
        select(func.count()).select_from(SiteHost).where(SiteHost.site_id == siteId)
    )
    a = await session.exec(count_statement)
    count = a.one()
    statement = (
        select(SiteHost).where(SiteHost.site_id == siteId)  # .offset(skip).limit(limit)
    )
    r = await session.exec(statement)
    items = r.all()

    return ListSiteHostsResponse(data=items, count=count)


@router.post("/hosts", response_model=SiteHostCreateResponse)
async def create_Site_host(
    *,
    session: AsyncSessionDep,
    current_user: CurrentUser,
    item_in: SiteHostCreateRequest,
) -> Any:
    """
    Create new site host.
    """
    site_host = SiteHost.model_validate(item_in)
    session.add(site_host)
    await session.commit()
    await session.refresh(site_host)
    return SiteHostCreateResponse(id=site_host.id)


@router.put("/hosts", response_model=SiteHostUpdateResponse)
async def update_site_host(
    *,
    session: AsyncSessionDep,
    current_user: CurrentUser,
    item_in: SiteHostUpdateRequest,
) -> Any:
    """
    Update site host.
    """
    item = await session.get(SiteHost, item_in.id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    if not current_user.is_superuser and (item.owner_id != current_user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    update_dict = item_in.model_dump(exclude_unset=True)
    item.sqlmodel_update(update_dict)
    session.add(item)
    await session.commit()
    await session.refresh(item)
    return SiteHostUpdateResponse(id=item.id)


@router.delete("/hosts/{id}", response_model=SiteHostDeleteResponse)
async def delete_site_host(
    *, session: AsyncSessionDep, current_user: CurrentUser, id: str
) -> Any:
    """
    Delete site host.
    """
    item = await session.get(SiteHost, id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    if not current_user.is_superuser and (item.owner_id != current_user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    await session.delete(item)
    await session.commit()
    return SiteHostDeleteResponse(id=item.id)


# tags 相关
@router.get("/tags/list", response_model=TagListResponse)
async def tab_list(
    *,
    session: AsyncSessionDep,
    siteId: uuid.UUID | None = None,
    query: str = Query(default=""),
    offset: int = 0,
    limit: int = Query(default=100, le=100),
):
    count_statement = select(func.count()).select_from(Tag).where(Tag.site_id == siteId)
    a = await session.exec(count_statement)
    count = a.one()
    statement = select(Tag).where(Tag.site_id == siteId).offset(offset).limit(limit)
    r = await session.exec(statement)
    items = r.all()

    return TagListResponse(data=items, count=count)
