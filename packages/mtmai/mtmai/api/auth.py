from datetime import timedelta
from typing import Annotated, Any
from urllib.parse import urlencode

import httpx
import structlog
from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from fastapi.security import OAuth2PasswordRequestForm
from mtmlib.github import get_github_user_data

from mtmai.core import coreutils, security
from mtmai.core.config import settings
from mtmai.core.security import get_password_hash
from mtmai.crud import curd, curd_account
from mtmai.deps import AsyncSessionDep, SessionDep, get_current_active_superuser
from mtmai.forge.app import DATABASE
from mtmai.forge.sdk.services.org_auth_token_service import create_org_api_token
from mtmai.models.models import Message, NewPassword, Token
from mtmai.utils import (
    generate_password_reset_token,
    generate_reset_password_email,
    send_email,
    verify_password_reset_token,
)

router = APIRouter()
LOG = structlog.get_logger()


@router.post("/login/access-token")
async def login_access_token(
    session: AsyncSessionDep, form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
) -> Token:
    """
    OAuth2 compatible token login, get an access token for future requests
    """
    user = await curd.authenticate(
        session=session, email=form_data.username, password=form_data.password
    )
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    if not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = Token(
        access_token=security.create_access_token(
            user.id, expires_delta=access_token_expires
        )
    )

    response = JSONResponse(content=access_token.model_dump())

    response.set_cookie(
        key=settings.COOKIE_ACCESS_TOKEN,
        value=access_token.access_token,
        httponly=True,
        secure=True,
        samesite="lax",
        max_age=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
    )

    return response


@router.post("/password-recovery/{email}")
async def recover_password(email: str, session: AsyncSessionDep) -> Message:
    """
    Password Recovery
    """
    user = await curd.get_user_by_email(session=session, email=email)

    if not user:
        raise HTTPException(
            status_code=404,
            detail="The user with this email does not exist in the system.",
        )
    password_reset_token = generate_password_reset_token(email=email)
    email_data = generate_reset_password_email(
        email_to=user.email, email=email, token=password_reset_token
    )
    send_email(
        email_to=user.email,
        subject=email_data.subject,
        html_content=email_data.html_content,
    )
    return Message(message="Password recovery email sent")


@router.post("/reset-password/")
async def reset_password(session: AsyncSessionDep, body: NewPassword) -> Message:
    """
    Reset password
    """
    email = verify_password_reset_token(token=body.token)
    if not email:
        raise HTTPException(status_code=400, detail="Invalid token")
    user = await curd.get_user_by_email(session=session, email=email)
    if not user:
        raise HTTPException(
            status_code=404,
            detail="The user with this email does not exist in the system.",
        )
    if not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    hashed_password = get_password_hash(password=body.new_password)
    user.hashed_password = hashed_password
    session.add(user)
    session.commit()
    return Message(message="Password updated successfully")


@router.post(
    "/password-recovery-html-content/{email}",
    dependencies=[Depends(get_current_active_superuser)],
    response_class=HTMLResponse,
)
async def recover_password_html_content(email: str, session: SessionDep) -> Any:
    """
    HTML Content for Password Recovery
    """
    user = await curd.get_user_by_email(session=session, email=email)

    if not user:
        raise HTTPException(
            status_code=404,
            detail="The user with this username does not exist in the system.",
        )
    password_reset_token = generate_password_reset_token(email=email)
    email_data = generate_reset_password_email(
        email_to=user.email, email=email, token=password_reset_token
    )

    return HTMLResponse(
        content=email_data.html_content, headers={"subject:": email_data.subject}
    )


@router.get("/auth/github/callback", include_in_schema=False)
async def github_oauth_callback(db: SessionDep, req: Request):
    # 打印请求的 query 参数
    print(f"Full URL: {req.url}")
    print(f"Query parameters: {req.query_params}")
    # 从请求中获取 GitHub OAuth 传回的 code 和 state 参数
    code = req.query_params.get("code")
    state = req.query_params.get("state", "")

    if not code:
        raise HTTPException(status_code=400, detail="Code not provided")

    client_id = settings.GITHUB_CLIENT_ID
    client_secret = settings.GITHUB_CLIENT_SECRET
    # 交换 code 获取 access token
    async with httpx.AsyncClient() as client:
        token_response = await client.post(
            "https://github.com/login/oauth/access_token",
            headers={
                "Accept": "application/json",
                "Content-Type": "application/json",
            },
            json={
                "client_id": client_id,
                "client_secret": client_secret,
                "code": code,
            },
        )
        token_data = token_response.json()

    access_token = token_data.get("access_token")
    if not access_token:
        raise HTTPException(status_code=400, detail="Failed to obtain access token")

    github_user_data = await get_github_user_data(access_token)
    user = curd_account.save_oauth_account(
        db=db, user_data=github_user_data, access_token=access_token
    )

    full_redirect_url = coreutils.abs_url(req, state)
    response = RedirectResponse(url=full_redirect_url)

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = Token(
        access_token=security.create_access_token(
            user.id, expires_delta=access_token_expires
        )
    )

    response.set_cookie(
        key=settings.COOKIE_ACCESS_TOKEN,
        value=access_token.access_token,
        httponly=True,
        secure=True,  # 在生产环境中建议开启
        samesite="Lax",  # 防止 CSRF 攻击
    )
    return response


@router.get("/auth/github/authorize", include_in_schema=False)
async def github_oauth_authorize(req: Request):
    client_id = settings.GITHUB_CLIENT_ID
    if not client_id:
        raise HTTPException(
            status_code=500, detail="Missing environment variable: GITHUB_CLIENT_ID"
        )

    next_url = req.query_params.get("next", "/")

    callback_path = f"{settings.API_V1_STR}/auth/github/callback"
    redirect_uri = coreutils.abs_url(req, callback_path)

    github_auth_url = "https://github.com/login/oauth/authorize?" + urlencode(
        {"client_id": client_id, "redirect_uri": redirect_uri, "state": next_url}
    )

    return RedirectResponse(github_auth_url)


@router.get("/get_org_api_token", tags=["myhelper"])
async def get_org_api_token():
    organization = await DATABASE.create_organization("org1")
    LOG.info(f"Created organization: {organization}")
    return await create_org_api_token(organization.organization_id)
