import os
from pathlib import Path
from typing import cast

from browser_use import Browser as BrowserUseBrowser
from browser_use import BrowserConfig as BrowseruseBrowserConfig
from browser_use import BrowserContextConfig
from browser_use.browser.context import BrowserContext
from crawl4ai.async_crawler_strategy import (
    AsyncCrawlerStrategy,
    AsyncPlaywrightCrawlerStrategy,
)
from crawl4ai.async_logger import AsyncLoggerBase

# from crawl4ai.browser_manager import BrowserManager
from loguru import logger
from mtmai.crawl4ai.async_configs import BrowserConfig
from mtmai.crawl4ai.async_webcrawler import AsyncWebCrawler

# from mtmai.mtlibs.browser_utils.browser_manager import BrowserManager
from playwright.async_api import Browser as PlaywrightBrowser
from playwright.async_api import Page


class MtBrowserConfig(BrowseruseBrowserConfig):
    pass


async def load_undetect_script():
    undetect_script = open(
        "packages/mtmai/mtmai/mtlibs/browser_utils/stealth_js/undetect_script.js", "r"
    ).read()
    return undetect_script


class MtBrowserContext(BrowserContext):
    async def _create_context(self, browser: PlaywrightBrowser):
        playwright_context = await super()._create_context(browser)
        # from undetected_playwright import Malenia

        # await Malenia.apply_stealth(playwright_context)

        # 额外的反检测脚本
        await playwright_context.add_init_script(await load_undetect_script())
        playwright_context.on(
            "page",
            self.on_page_created,
        )

        return playwright_context

    async def on_page_created(self, page: Page):
        # 这行没实际生效, 原因未知
        logger.info(f"on_page_created: {page}")


class MtBrowserManager(AsyncWebCrawler):
    """
    设计备忘:
        1: crawl4ai 的 AsyncWebCrawler 设计比较合理, 因此这里跟浏览器相关的上下文直接复用这个类
        2: 增加功能: 让 browser use 的浏览器上下文共享 crawl4ai 的浏览器上下文
    """

    def __init__(
        self,
        crawler_strategy: AsyncCrawlerStrategy = None,
        config: BrowserConfig = None,
        base_directory: str = str(os.getenv("CRAWL4_AI_BASE_DIRECTORY", Path.home())),
        thread_safe: bool = False,
        logger: AsyncLoggerBase = None,
        **kwargs,
    ):
        super().__init__(
            crawler_strategy=crawler_strategy,
            config=config,
            base_directory=base_directory,
            thread_safe=thread_safe,
            logger=logger,
        )
        # browser use 的浏览器配置,共享 crawl4ai 的浏览器配置
        crawler_strategy = cast(AsyncPlaywrightCrawlerStrategy, self.crawler_strategy)
        config = crawler_strategy.browser_manager.config
        self.browseruse_browser = BrowserUseBrowser(
            config=MtBrowserConfig(
                headless=False,
                disable_security=False,
                cdp_url=f"http://{config.host}:{config.debugging_port}",
            )
        )

    async def create_browser_use_context(self):
        browser_context = MtBrowserContext(
            browser=self.browseruse_browser,
            config=BrowserContextConfig(
                disable_security=False,  # 如果禁用了 csp, 一般会被识别为机器人
                # user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36",
                _force_keep_context_alive=True,
            ),
        )
        return browser_context
