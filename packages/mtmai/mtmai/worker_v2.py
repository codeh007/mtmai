"""
基于 pgmq 消息队列的 worker 入口
"""

import asyncio
import logging
from typing import Optional

from loguru import logger
from sqlalchemy import text
from sqlalchemy.exc import ArgumentError

from mtmai.core.config import settings
from mtmai.db.db import get_async_session


class WorkerV2:
    def __init__(
        self,
        *,
        db_url: str,
    ) -> None:
        self.db_url = db_url
        self._running = False
        self._task: Optional[asyncio.Task] = None
        try:
            # db_engine = create_engine(db_url)
            # self.db_engine: Engine = db_engine
            pass
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

    async def _get_one_message(self):
        """
        获取一条消息
        """
        async with get_async_session() as session:
            result_data = (
                await session.exec(
                    text("SELECT * FROM taskmq_pull(:queue_name, :consumer_id)"),
                    params={"queue_name": "aa", "consumer_id": "bb"},
                )
            ).all()
            await session.commit()
            return result_data

    async def _ack_message(self, msg_id: int) -> None:
        """
        确认消息
        """
        async with get_async_session() as session:
            await session.exec(
                text("SELECT taskmq_submit_result(:msg_id)"),
                params={"msg_id": msg_id},
            )
            await session.commit()

    async def _consume_messages(self) -> None:
        """
        消费消息的主循环
        """
        wait_seconds = 5
        while self._running:
            try:
                result_data = await self._get_one_message()
                if len(result_data) == 0:
                    await asyncio.sleep(1)
                    continue

                for msg_tuple in result_data:
                    try:
                        msg_id = msg_tuple.msg_id
                        message_obj = msg_tuple.message
                        payload = message_obj.get("input")
                        if not payload:
                            raise ValueError("input 为空")
                        result = await self.on_message(msg_id, payload)
                        await self._ack_message(msg_id)
                        logger.info(f"任务完成: {msg_id}")

                    except Exception as e:
                        logger.error(f"任务出错: error={str(e)}")

            except Exception as e:
                if "Connection timed out" in str(
                    e
                ) or "could not receive data from server" in str(e):
                    logger.warning(f"数据库连接超时,将在{wait_seconds}秒后重试: {e}")
                    await asyncio.sleep(wait_seconds)
                    continue
                logger.error(f"消费消息错误: {e}")
                await asyncio.sleep(1)

    async def stop(self) -> None:
        """
        停止 worker
        """
        if not self._running:
            logger.warning("Worker is not running")
            return

        logging.info(f"Stopping worker for queue: {self.queue_name}")
        self._running = False

        if self._task:
            self._task.cancel()
            try:
                await self._task
            except asyncio.CancelledError:
                pass
            self._task = None

    async def on_message(self, msg_id: str, payload: dict) -> None:
        """
        处理消息
        """
        logger.info(f"on_message\t{msg_id}\t{payload}")
        return {
            "result": "success",
            "some_data": "some_data1111",
        }
