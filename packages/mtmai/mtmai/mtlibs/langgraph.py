from typing import Literal

from mtmai.core.config import settings


def get_langgraph_checkpointer(
    checkpointer_type: Literal["memory", "postgres"] = "memory",
):
    # if checkpointer_type == "postgres":
    #     return get_async_sqlite_checkpointer()
    from langgraph.checkpoint.memory import MemorySaver

    memory = MemorySaver()
    return memory


def get_async_postgres_checkpointer():
    from langgraph.checkpoint.postgres.aio import AsyncPostgresSaver
    from psycopg_pool import AsyncConnectionPool

    connection_kwargs = {
        "autocommit": True,
        "prepare_threshold": 0,
    }
    poll2 = AsyncConnectionPool(
        # Example configuration
        conninfo=settings.MTMAI_DATABASE_URL,
        max_size=20,
        kwargs=connection_kwargs,
    )
    # conn = poll2.connection()
    checkpointer = AsyncPostgresSaver(poll2)
    return checkpointer


def get_postgres_checkpointer():
    from langgraph.checkpoint.postgres import PostgresSaver
    from psycopg_pool import ConnectionPool

    connection_kwargs = {
        "autocommit": True,
        "prepare_threshold": 0,
    }
    poll2 = ConnectionPool(
        # Example configuration
        conninfo=settings.MTMAI_DATABASE_URL,
        max_size=20,
        kwargs=connection_kwargs,
    )
    # conn = poll2.connection()
    checkpointer = PostgresSaver(poll2)

    checkpointer.setup()

    return checkpointer
