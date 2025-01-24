import uuid
from typing import Any

import structlog
from fastapi import HTTPException

# from mtmai.db.db import get_async_session
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from mtmai.core.security import get_password_hash, verify_password
from mtmai.models.models import User, UserCreate, UserUpdate

LOG = structlog.get_logger()


def _clean_result(obj):
    """Recursively change UUID -> str and serialize dictionaries"""
    if isinstance(obj, dict):
        return {k: _clean_result(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [_clean_result(item) for item in obj]
    elif isinstance(obj, uuid.UUID):
        return str(obj)
    return obj


# async def execute_sql(
#     query: str, parameters: dict
# ) -> Union[List[Dict[str, Any]], int, None]:
#     parameterized_query = text(query)
#     async with get_async_session() as session:
#         try:
#             # await session.begin()
#             result = await session.exec(parameterized_query, parameters)
#             # await session.commit()
#             if result.returns_rows:
#                 json_result = [dict(row._mapping) for row in result.fetchall()]
#                 clean_json_result = _clean_result(json_result)
#                 return clean_json_result
#             else:
#                 return result.rowcount
#         except SQLAlchemyError as e:
#             await session.rollback()
#             LOG.warn(f"An error occurred: {e}")
#             return None
#         except Exception as e:
#             await session.rollback()
#             LOG.warn(f"An unexpected error occurred: {e}")
#             return None


# @cached(ttl=300)
# async def get_user_by_id2(user_id: str) -> User | None:
#     if not user_id:
#         return None
#     async with get_async_session() as session:
#         statement = select(User).where(User.id == user_id)
#         result = await session.exec(statement)
#         return result.first()


# async def get_organization_by_user_id(user_id: str | uuid.UUID):
#     from mtmai.forge.app import DATABASE

#     user = await get_user_by_id2(user_id)
#     organization_id = user.organization_id

#     organization = await DATABASE.get_organization(organization_id)
#     return organization


async def register_user(session: AsyncSession, user_in: UserCreate) -> User:
    from mtmai.forge.app import DATABASE

    new_organization = await DATABASE.create_organization(
        organization_name=user_in.username,
        webhook_callback_url="",
        max_steps_per_run="100",
        max_retries_per_step="3",
        domain="",
    )

    user = await get_user_by_email(session=session, email=user_in.email)
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this email already exists in the system",
        )
    user_create = UserCreate.model_validate(user_in)
    user_create.organization_id = new_organization.organization_id
    user = await create_user(session=session, user_create=user_create)

    return user


async def create_user(*, session: AsyncSession, user_create: UserCreate) -> User:
    db_obj = User.model_validate(
        user_create, update={"hashed_password": get_password_hash(user_create.password)}
    )
    session.add(db_obj)
    await session.commit()
    await session.refresh(db_obj)
    return db_obj


async def update_user(
    *, session: AsyncSession, db_user: User, user_in: UserUpdate
) -> Any:
    user_data = user_in.model_dump(exclude_unset=True)
    extra_data = {}
    if "password" in user_data:
        password = user_data["password"]
        hashed_password = get_password_hash(password)
        extra_data["hashed_password"] = hashed_password
    db_user.sqlmodel_update(user_data, update=extra_data)
    session.add(db_user)
    await session.commit()
    await session.refresh(db_user)
    return db_user


async def get_user_by_email(*, session: AsyncSession, email: str) -> User | None:
    statement = select(User).where(User.email == email)
    result = await session.exec(statement)
    session_user = result.first()
    return session_user


async def get_user_by_username(*, session: AsyncSession, username: str) -> User | None:
    statement = select(User).where(User.username == username)
    result = await session.exec(statement)
    return result.first()


async def get_user_by_id(*, session: AsyncSession, id: str) -> User | None:
    if not id:
        return None
    statement = select(User).where(User.id == id)
    result = await session.exec(statement)
    return result.first()


async def authenticate(
    *, session: AsyncSession, email: str, password: str
) -> User | None:
    db_user = await get_user_by_email(session=session, email=email)
    if not db_user:
        return None
    if not verify_password(password, db_user.hashed_password):
        return None
    return db_user


# async def create_item(
#     *, session: AsyncSession, item_in: ItemCreate, owner_id: str
# ) -> Item:
#     db_item = Item.model_validate(item_in, update={"owner_id": owner_id})
#     session.add(db_item)
#     await session.commit()
#     await session.refresh(db_item)
#     return db_item
