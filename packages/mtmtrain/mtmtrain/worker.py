import asyncio
import logging

from mtmlib import env
from mtmlib.queue.mtqueue_client import MtQueueClient
from mtmlib.queue.queue import MessagePublic

from mtmtrain.core.config import settings

logger = logging.getLogger("mttrain_worker")


def worker_start():
    logger.info("worker start")
    if env.in_jupyter_notebook():
        print(" run @ ipython")
    queue_client = MtQueueClient(backend=settings.MTMAI_API_BASE)

    queue_client.register_consumer(queue_name="test1", consumer_fn=msg_handler1)
    asyncio.run(queue_client.run())

    logger.info("worker end!")


def msg_handler1(msg: MessagePublic):
    logger.info("msg_handler1 处理消息 %s", msg)
