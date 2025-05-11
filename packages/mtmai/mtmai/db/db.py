import logging
import time
from contextlib import asynccontextmanager
from functools import wraps
from typing import Callable, TypeVar, cast

from psycopg_pool import AsyncConnectionPool
from sqlalchemy.exc import DisconnectionError, OperationalError, SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine
from sqlmodel.ext.asyncio.session import AsyncSession

from mtmai.core.config import settings

logger = logging.getLogger(__name__)


def fix_conn_str(conn_str: str) -> str:
    if not str(conn_str).startswith("postgresql+psycopg"):
        conn_str = str(conn_str).replace("postgresql", "postgresql+psycopg")
    return conn_str


# 全局连接池对象
pool: AsyncConnectionPool | None = None
async_engine: AsyncEngine | None = None


async def get_async_engine():
    global async_engine
    if async_engine is not None:
        return async_engine
    if settings.MTM_DATABASE_URL is None:
        raise ValueError("MTM_DATABASE_URL environment variable is not set")  # noqa: EM101, TRY003

    # 创建连接池配置
    pool_options = {
        "pool_size": settings.MTM_DATABASE_POOL_SIZE,
        "max_overflow": 10,  # 允许的最大溢出连接数
        "pool_timeout": 30,  # 连接池获取连接的超时时间
        "pool_recycle": 1800,  # 连接在池中重用的时间限制
        "pool_pre_ping": True,  # 在使用连接前先测试连接是否有效
    }

    async_engine = create_async_engine(
        fix_conn_str(settings.MTM_DATABASE_URL),
        #    echo=True,# echo 会打印所有sql语句，影响性能
        future=True,
        **pool_options,
    )
    return async_engine


@asynccontextmanager
async def get_async_session():
    engine = await get_async_engine()
    async with AsyncSession(engine) as session:
        try:
            yield session
        finally:
            await session.close()


T = TypeVar("T")


def with_db_retry(max_retries: int = 3, retry_delay: float = 1.0):
    """装饰器：为数据库操作添加重试机制

    Args:
        max_retries: 最大重试次数
        retry_delay: 重试间隔（秒）
    """

    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        @wraps(func)
        def wrapper(*args, **kwargs) -> T:
            last_exception = None
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except (OperationalError, DisconnectionError) as e:
                    last_exception = e
                    if attempt < max_retries - 1:
                        logger.warning(
                            f"Database operation failed (attempt {attempt + 1}/{max_retries}): {str(e)}. "
                            f"Retrying in {retry_delay} seconds..."
                        )
                        time.sleep(retry_delay)
                    else:
                        logger.error(
                            f"Database operation failed after {max_retries} attempts: {str(e)}"
                        )
                        raise
                except SQLAlchemyError as e:
                    logger.error(f"Database error: {str(e)}")
                    raise
            raise last_exception

        return cast(Callable[..., T], wrapper)

    return decorator
