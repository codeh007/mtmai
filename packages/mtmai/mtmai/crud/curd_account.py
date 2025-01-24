import logging

import jwt
from pydantic import ValidationError
from sqlmodel import Session, select

from mtmai.core import security
from mtmai.core.config import settings
from mtmai.crud.curd import create_user, get_user_by_email
from mtmai.models.models import (
    Account,
    AccountBase,
    TokenPayload,
    User,
    UserCreate,
)

logger = logging.getLogger()


class TokenDecodeError(Exception):
    def __init__(self, detail: str):
        self.detail = detail


def verify_token(token: str) -> TokenPayload:
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[security.ALGORITHM]
        )
        return TokenPayload(**payload)
    except jwt.InvalidTokenError:
        raise TokenDecodeError("Invalid token")
    except jwt.ExpiredSignatureError:
        raise TokenDecodeError("Token has expired")
    except jwt.DecodeError:
        raise TokenDecodeError("Could not decode token")
    except ValidationError:
        raise TokenDecodeError("Invalid token payload")


class AccountCreate(AccountBase):
    pass


def create_account(
    *, session: Session, item_in: AccountCreate, owner_id: str
) -> Account:
    account = Account.model_validate(item_in, update={"owner_id": owner_id})
    session.add(account)
    session.commit()
    session.refresh(account)
    return account


def update_account(*, session: Session, account_id: str, token: str) -> Account:
    account = session.get(Account, account_id)
    if not account:
        raise ValueError(f"Account with ID {account_id} not found")
    account.token = token
    session.commit()
    session.refresh(account)
    return account


class AccountUpdate(AccountBase):
    pass


async def save_oauth_account(*, db: Session, user_data: any, access_token: str) -> User:
    """保存 oauth 登录成功后的 用户凭证到数据库"""
    username = user_data["login"]
    email = username + "@github.com"
    user = await get_user_by_email(session=db, email=email)
    if not user:
        logger.info("oauth 找不到 本地用户, 创建")
        user_in = UserCreate(
            email=email, password=settings.MEMBER_USER_DEFAULT_PASSWORD
        )
        user = create_user(session=db, user_create=user_in)

    exists_account = get_account_by_user_id(session=db, owner_id=user.id)
    if not exists_account:
        logger.info("创建新的 OAuth 账户")
        create_account(
            session=db,
            item_in=AccountCreate(
                token=access_token,
                provider="github",
            ),
            owner_id=user.id,
        )
    else:
        logger.info("更新现有的 OAuth 账户信息")
        update_account(session=db, account_id=exists_account.id, token=access_token)

    return user


def get_account_by_user_id(*, session: Session, owner_id: str) -> Account:
    statement = select(Account).where(Account.owner_id == owner_id)
    account_item = session.exec(statement).first()
    return account_item
