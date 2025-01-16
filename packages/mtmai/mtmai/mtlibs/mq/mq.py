from typing import Any
from urllib.parse import urlparse

from fastapi.encoders import jsonable_encoder
from tembo_pgmq_python.async_queue import PGMQueue

from mtmai.core.config import settings
from mtmai.core.logging import get_logger

logger = get_logger()


class MtTaskMQ:
    """
    工作流任务队列专用消息总线
    文档： https://github.com/tembo-io/pgmq/blob/main/tembo-pgmq-python/README.md
    """

    def __init__(self, thread_id: str):
        self.thread_id = thread_id
        self.mq = None

    async def init(self, thread_id: str):
        if self.mq is not None:
            return  # Already initialized

        self.thread_id = thread_id
        db_url = settings.MTMAI_DATABASE_URL
        parsed_url = urlparse(db_url)
        self.mq = PGMQueue(
            host=parsed_url.hostname,
            port=parsed_url.port or 5432,
            database=parsed_url.path[1:],  # Remove leading '/'
            username=parsed_url.username,
            password=parsed_url.password,
        )
        await self.mq.init()

        self.queue_name = f"chat_event_{self.thread_id.replace('-', '_')}"
        try:
            # create_partitioned_queue 似乎需要安装其他插件
            # Failed to create partitioned queue chat_event_4e426405_acc9_467f_8633_c4120419517c: function pgmq.create(unknown, text, text) does not exist
            # await self.mq.create_partitioned_queue(
            #     self.queue_name, partition_interval=10000
            # )
            await self.mq.create_queue(self.queue_name)
        except Exception as e:
            logger.error(f"Failed to create queue {self.queue_name}: {e}")

    async def send_event(self, message: Any | list):
        if self.mq is None:
            await self.init()

        if isinstance(message, list):
            messages = message
            messages_to_send = [jsonable_encoder(message) for message in messages]
            await self.mq.send_batch(self.queue_name, messages_to_send)
        else:
            await self.mq.send(self.queue_name, jsonable_encoder(message))

    async def pull_messages(
        self, qty: int = 5, max_poll_seconds: int = 5, poll_interval_ms: int = 100
    ):
        logger.info(
            f"pull_messages {self.queue_name} {qty} {max_poll_seconds} {poll_interval_ms}"
        )
        read_messages: list[Any] = await self.mq.read_with_poll(
            # read_messages: list[Message] = self.read_with_poll(
            self.queue_name,
            vt=30,
            qty=qty,
            max_poll_seconds=max_poll_seconds,
            poll_interval_ms=poll_interval_ms,
        )
        for message in read_messages:
            print(message)
            yield message
