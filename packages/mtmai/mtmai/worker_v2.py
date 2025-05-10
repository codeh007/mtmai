"""
基于 pgmq 消息队列的 worker 入口
"""

import logging

from sqlalchemy import Engine, create_engine
from sqlalchemy.exc import ArgumentError


class WorkerV2:
    def __init__(
        self,
        *,
        db_url: str,
        pgmq_queue_name: str,
        pgmq_consumer_group: str = "default_group",
    ) -> None:
        self.db_url = db_url
        self.pgmq_queue_name = pgmq_queue_name
        self.pgmq_consumer_group = pgmq_consumer_group
        try:
            db_engine = create_engine(db_url)
            self.db_engine: Engine = db_engine
        except Exception as e:
            if isinstance(e, ArgumentError):
                raise ValueError(
                    f"Invalid database URL format or argument '{db_url}'."
                ) from e
            if isinstance(e, ImportError):
                raise ValueError(
                    f"Database related module not found for URL '{db_url}'."
                ) from e
            raise ValueError(
                f"Failed to create database engine for URL '{db_url}'"
            ) from e

    async def start(self) -> None:
        """
        启动 worker
        """
        logging.info(f"Starting worker for queue: {self.pgmq_queue_name}")

        # 创建 pgmq 客户端

    async def stop(self) -> None:
        """
        停止 worker
        """
        logging.info(f"Stopping worker for queue: {self.pgmq_queue_name}")
