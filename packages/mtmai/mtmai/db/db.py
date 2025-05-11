from contextlib import asynccontextmanager

from psycopg_pool import AsyncConnectionPool
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine
from sqlmodel.ext.asyncio.session import AsyncSession

from mtmai.core.config import settings


def fix_conn_str(conn_str: str) -> str:
    if not str(conn_str).startswith("postgresql+psycopg"):
        conn_str = str(conn_str).replace("postgresql", "postgresql+psycopg")
    return conn_str


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
            conninfo=settings.MTM_DATABASE_URL,
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
    if settings.MTM_DATABASE_URL is None:
        raise ValueError("MTM_DATABASE_URL environment variable is not set")  # noqa: EM101, TRY003

    return create_async_engine(
        fix_conn_str(settings.MTM_DATABASE_URL),
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
