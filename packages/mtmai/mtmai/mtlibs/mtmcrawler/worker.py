import asyncio
import json

from sqlalchemy.ext.asyncio import AsyncEngine

from mtmai.core.logging import get_logger
from mtmai.mtlibs.mq.pq_queue import AsyncPGMQueue
from mtmai.mtlibs.mtmcrawler.mtmcrawler import MTCrawlerPageParams, _fetch_page_html
from mtmlib.queue.queue import Message

logger = get_logger()

mtm_crawl_queue = "mtm-crawl-queue"


class CrawlWorker:
    def __init__(self, mq: AsyncPGMQueue, engine: AsyncEngine):
        self.mq = mq
        self.db = engine
        self.is_running = False

    async def start(self):
        # logger.info("🕷️ 🟢 Start MTM crawler worker ")
        self.is_running = True

        asyncio.create_task(self._pull_messages())

    async def stop(self):
        logger.info("🕷️ 🛑 Stop MTM crawler worker ")
        self.is_running = False

    async def _pull_messages(self):
        logger.info(f"🕷️ 🟢 pull_messages from {mtm_crawl_queue}")
        await self.mq.create_queue(queue=mtm_crawl_queue)
        while self.is_running:
            try:
                msg = await self.mq.read(queue=mtm_crawl_queue)
                if msg:
                    await self._handle_message(msg)
                else:
                    await asyncio.sleep(1)
            except Exception as e:
                logger.error(f"🕷️ 🔴 pull_messages error: {e}")
                await asyncio.sleep(1)

    async def _handle_message(self, msg: Message):
        # logger.info(f"读取到消息队列的消息 : {msg.msg_id}")
        params = MTCrawlerPageParams(**json.loads(msg.message))
        # logger.info(f"处理消息队列的消息 : {params.url}")
        await self.crawl_page(params)
        await self.mq.ack(mtm_crawl_queue, msg.msg_id)
        logger.debug(f"处理消息队完成{msg.msg_id}")

    async def enqueue_url(self, site_id: str, url: str):
        params = MTCrawlerPageParams(site_id=site_id, url=url, current_depth=0)
        message = json.dumps(params.model_dump())
        await self.mq.send(mtm_crawl_queue, message)
        logger.info(f"发送消息队列的消息 : {params.url} 完成")

    async def crawl_page(self, params: MTCrawlerPageParams):
        """
        爬取一个页面并建立页面索引
        """
        html = await _fetch_page_html(params.url)
        if html is None:
            return None
        logger.info(f"crawl_page: {len(html)}, {params.url}")

        # page_item = MTCrawlPage(
        #     site_id=params.site_id,
        #     url=params.url,
        #     depth=params.current_depth,
        #     title="",
        #     description="",
        #     keywords="",
        #     author="fake_author",
        #     copyright="fake_copyright",
        # )
        # async with AsyncSession(self.db) as session:
        #     await session.add(page_item)
        #     await session.commit()
        # return update_item
        return None
