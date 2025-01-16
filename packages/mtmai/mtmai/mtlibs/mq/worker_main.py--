import asyncio
import logging
import threading
from dataclasses import field

from mtmai.core.config import settings
from mtmai.mtlibs.mq.pq_queue import AsyncPGMQueue, PGMQueue

logger = logging.getLogger()
# 当消息读取次数大于这个值, 就当作永久失败, 放入死信队列
max_read_count = 10


def get_queue():
    return PGMQueue(settings.DATABASE_URL)


def get_async_queue():
    return AsyncPGMQueue(settings.DATABASE_URL)


class WorkerMain:
    """worker 主入口"""

    def __init__(self):
        self.queue = PGMQueue(settings.DATABASE_URL)

    # 存储队列名和 处理函数的关系
    handler_dict: dict[str, callable] = field(default_factory=dict)

    def register_consumer(self, *, queue_name, consumer_fn):
        self.handler_dict[queue_name] = consumer_fn

    def run(self):
        threading.Thread(target=self._run_thread).start()

    def _run_thread(self):
        """Run the worker's main logic in an event loop."""
        logger.info("启动worker 主进程")
        asyncio.run(self._start_consumers())

    async def _start_consumers(self):
        """Start all consumers concurrently."""
        tasks = [
            self._consume_messages(queue_name, consumer_fn)
            for queue_name, consumer_fn in self.handler_dict.items()
        ]
        await asyncio.gather(*tasks)

    async def _consume_messages(self, queue_name: str, consumer_fn: callable):
        """Consume messages from a queue and process them using the registered consumer function."""
        while True:
            messages = self.queue.read_batch(queue_name)
            if messages:
                for msg in messages:
                    try:
                        consumer_fn(msg.message)
                        self.queue.delete(queue_name, msg.msg_id)
                    except Exception as e:  # noqa: BLE001
                        logger.info("Message processing failed:  %s", e)
                        if msg.read_ct > max_read_count:  # Failed more than 3 times
                            # TODO: 放入死信队列
                            # dlq.send("dead_letter_queue", msg.message)  # Move to DLQ
                            self.queue.delete(queue_name, msg.msg_id)
                        else:
                            logger.info("Retrying message %s", msg.msg_id)
            await asyncio.sleep(2)
