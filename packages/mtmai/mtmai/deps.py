from collections.abc import Generator
from typing import Annotated, AsyncGenerator

import jwt
from fastapi import Depends, HTTPException, Request, status
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import InvalidTokenError
from langgraph.checkpoint.postgres.aio import AsyncPostgresSaver
from pydantic import ValidationError
from sqlmodel import Session
from sqlmodel.ext.asyncio.session import AsyncSession

from mtmai.core import security
from mtmai.core.config import HEADER_SITE_HOST, settings
from mtmai.crud.curd_site import get_site_domain
from mtmai.db.db import engine, get_async_engine, get_checkpointer
from mtmai.models.models import TokenPayload, User
from mtmai.models.site import Site

reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/login/access-token",
    auto_error=False,  # 没有 token header 时不触发异常
)


def get_db() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session


async def get_asession() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSession(get_async_engine()) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_db)]

AsyncSessionDep = Annotated[AsyncSession, Depends(get_asession)]


TokenDep = Annotated[str, Depends(reusable_oauth2)]


def get_host_from_request(request: Request):
    host = request.headers.get("Host")
    return host


HostDep = Annotated[str, Depends(get_host_from_request)]


def get_current_user(session: SessionDep, token: TokenDep, request: Request) -> User:
    token = token or request.cookies.get(settings.COOKIE_ACCESS_TOKEN)
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[security.ALGORITHM]
        )
        token_data = TokenPayload(**payload)
    except (InvalidTokenError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )
    user = session.get(User, token_data.sub)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return user


CurrentUser = Annotated[User, Depends(get_current_user)]


def get_current_active_superuser(current_user: CurrentUser) -> User:
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=403, detail="The user doesn't have enough privileges"
        )
    return current_user


def get_optional_current_user(
    session: SessionDep, token: TokenDep, request: Request
) -> User | None:
    token = token or request.cookies.get(settings.COOKIE_ACCESS_TOKEN)
    if not token:
        return None
    try:
        return get_current_user(session, token, request)
    except HTTPException:
        return None


OptionalUserDep = Annotated[User | None, Depends(get_optional_current_user)]


CheckPointerDep = Annotated[AsyncPostgresSaver, Depends(get_checkpointer)]


async def get_site(session: AsyncSessionDep, request: Request) -> Site:
    """
    根据入站域名获取对应是site 对象
    """
    income_domain = request.headers.get(HEADER_SITE_HOST)
    if not income_domain:
        # 尝试从多个来源获取前端域名
        # 1. 检查反向代理头
        if "X-Forwarded-Host" in request.headers:
            income_domain = request.headers["X-Forwarded-Host"]
        # 2. 检查 Referer 头
        elif "Referer" in request.headers:
            from urllib.parse import urlparse

            referer = request.headers["Referer"]
            income_domain = urlparse(referer).netloc
        # 3. 检查 Origin 头
        elif "Origin" in request.headers:
            from urllib.parse import urlparse

            origin = request.headers["Origin"]
            income_domain = urlparse(origin).netloc
        # 4. 如果以上都失败，使用 Host 头作为后备
        else:
            income_domain = request.headers.get("Host")

    if income_domain:
        site = await get_site_domain(session, income_domain)
        return site
    else:
        raise HTTPException(status_code=400, detail="Unable to determine site domain")


SiteDep = Annotated[Site, Depends(get_site)]
SiteDep = Annotated[Site, Depends(get_site)]
