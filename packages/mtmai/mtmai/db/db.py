# import logging
# import uuid
# from typing import Any, Dict, List, Union

from contextlib import asynccontextmanager

from psycopg_pool import AsyncConnectionPool

# from sqlalchemy import text
# from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine
from sqlmodel import Session, create_engine, select
from sqlmodel.ext.asyncio.session import AsyncSession

from mtmai.core.config import settings
from mtmai.crud import curd
from mtmai.models.models import User, UserCreate


def init_db(session: Session) -> None:
    user = session.exec(
        select(User).where(User.email == settings.FIRST_SUPERUSER)
    ).first()
    if not user:
        user_in = UserCreate(
            email=settings.FIRST_SUPERUSER,
            password=settings.FIRST_SUPERUSER_PASSWORD,
            is_superuser=True,
        )
        user = curd.create_user(session=session, user_create=user_in)


engine = None


def fix_conn_str(conn_str: str) -> str:
    if not str(conn_str).startswith("postgresql+psycopg"):
        conn_str = str(conn_str).replace("postgresql", "postgresql+psycopg")
    return conn_str


def get_engine():
    global engine
    if engine is not None:
        return engine
    if settings.MTMAI_DATABASE_URL is None:
        raise ValueError("MTMAI_DATABASE_URL environment variable is not set")  # noqa: EM101, TRY003
    return create_engine(
        settings.MTMAI_DATABASE_URL,
        connect_args={"sslmode": "require"},
        pool_recycle=300,
    )


engine = get_engine()


# 全局连接池对象
pool: AsyncConnectionPool | None = None


async def get_checkpointer():
    from langgraph.checkpoint.postgres.aio import AsyncPostgresSaver

    global pool
    if not pool or pool.closed:
        connection_kwargs = {
            "autocommit": True,
            "prepare_threshold": 0,
        }
        pool = AsyncConnectionPool(
            conninfo=settings.MTMAI_DATABASE_URL,
            max_size=20,
            kwargs=connection_kwargs,
        )
        await pool.open()
    checkpointer = AsyncPostgresSaver(pool)
    yield checkpointer


async_engine: AsyncEngine | None = None


def get_async_engine():
    global async_engine
    if async_engine is not None:
        return async_engine
    if settings.MTMAI_DATABASE_URL is None:
        raise ValueError("DATABASE_URL environment variable is not set")  # noqa: EM101, TRY003

    return create_async_engine(
        fix_conn_str(settings.MTMAI_DATABASE_URL),
        #    echo=True,# echo 会打印所有sql语句，影响性能
        future=True,
    )


@asynccontextmanager
async def get_async_session():
    engine = get_async_engine()
    async with AsyncSession(engine) as session:
        try:
            yield session
        finally:
            await session.close()
