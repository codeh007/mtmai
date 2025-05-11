"""
基于 pgmq 消息队列的 worker 入口
"""

import asyncio
import logging
from typing import Optional

from loguru import logger
from pgmq_sqlalchemy import PGMQueue
from sqlalchemy import Engine, create_engine
from sqlalchemy.exc import ArgumentError

from mtmai.core.config import settings


class WorkerV2:
    def __init__(
        self,
        *,
        db_url: str,
    ) -> None:
        self.db_url = db_url
        # self.pgmq_queue_name = pgmq_queue_name
        # self.pgmq_consumer_group = pgmq_consumer_group
        self._running = False
        self._task: Optional[asyncio.Task] = None
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
        if self._running:
            logger.warning("Worker is already running")
            return

        logging.info(f"Starting worker for queue: {settings.QUEUE_SHORTVIDEO_COMBINE}")
        self._running = True
        self._task = asyncio.create_task(self._consume_messages())

    async def start_block(self) -> None:
        """
        阻塞启动 worker
        """
        await self.start()
        await self._consume_messages()

    async def _consume_messages(self) -> None:
        """
        消费消息的主循环
        """
        pgmq = PGMQueue(dsn=self.db_url)

        queues = pgmq.list_queues()
        # logger.info(f"队列列表: {queues}")
        if settings.QUEUE_SHORTVIDEO_COMBINE not in queues:
            logger.info(f"队列 {settings.QUEUE_SHORTVIDEO_COMBINE} 不存在,现在创建")

            pgmq.create_queue(settings.QUEUE_SHORTVIDEO_COMBINE)

        while self._running:
            try:
                # read a single message
                msg = pgmq.read(settings.QUEUE_SHORTVIDEO_COMBINE)
                if not msg:
                    await asyncio.sleep(1)
                    continue

                logger.info(f"收到消息: {msg}")
                try:
                    # TODO: 处理消息
                    logger.info(f"处理消息: {msg.message}")
                except Exception as e:
                    logger.error(f"处理消息失败: {e}")
                    # 设置消息可见性超时,让消息重新入队
                    pgmq.set_vt(self.pgmq_queue_name, msg.msg_id, 30)
                finally:
                    # 删除已处理的消息
                    pgmq.delete(self.pgmq_queue_name, msg.msg_id)
            except Exception as e:
                logger.error(f"消费消息时发生错误: {e}")
                await asyncio.sleep(1)

    async def stop(self) -> None:
        """
        停止 worker
        """
        if not self._running:
            logger.warning("Worker is not running")
            return

        logging.info(f"Stopping worker for queue: {self.pgmq_queue_name}")
        self._running = False

        if self._task:
            self._task.cancel()
            try:
                await self._task
            except asyncio.CancelledError:
                pass
            self._task = None
