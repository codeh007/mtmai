import asyncio
import os
from pathlib import Path
from typing import cast

from browser_use import Browser as BrowserUseBrowser
from browser_use import BrowserConfig as BrowseruseBrowserConfig
from browser_use import BrowserContextConfig
from browser_use.browser.context import BrowserContext
from browser_use.browser.views import BrowserState
from browser_use.utils import time_execution_sync
from crawl4ai.async_configs import BrowserConfig
from crawl4ai.async_crawler_strategy import (
    AsyncCrawlerStrategy,
    AsyncPlaywrightCrawlerStrategy,
)
from crawl4ai.async_webcrawler import AsyncWebCrawler
from crawl4ai.types import AsyncLoggerBase
from loguru import logger
from mtmai.core.config import settings
from playwright.async_api import Browser as PlaywrightBrowser
from playwright.async_api import Page


class MtBrowserConfig(BrowseruseBrowserConfig):
    pass


class MtBrowseruseContext(BrowserContext):
    async def _create_context(self, browser: PlaywrightBrowser):
        playwright_context = await super()._create_context(browser)
        # from undetected_playwright import Malenia

        # await Malenia.apply_stealth(playwright_context)

        # 额外的反检测脚本
        async def load_undetect_script():
            undetect_script = open(
                "packages/mtmai/mtmai/mtlibs/browser_utils/stealth_js/undetect_script.js",
                "r",
            ).read()
            return undetect_script

        await playwright_context.add_init_script(await load_undetect_script())

        await playwright_context.add_cookies(
            [
                {
                    "name": "cookiesEnabled2222detector",
                    "value": "true",
                    "url": "https://bot-detector.rebrowser.net",
                }
            ]
        )
        playwright_context.on("page", self.on_page_created)

        return playwright_context

    async def on_page_created(self, page: Page):
        # 这行没实际生效, 原因未知
        logger.info(f"on_page_created: {page}")

    @time_execution_sync(
        "--get_state"
    )  # This decorator might need to be updated to handle async
    async def get_state(self) -> BrowserState:
        """Get the current state of the browser"""
        await self._wait_for_page_and_frames_load()
        session = await self.get_session()
        session.cached_state = await self._update_state()

        # Save cookies if a file is specified
        # if self.config.cookies_file:
        asyncio.create_task(self.save_cookies())

    async def save_cookies(self):
        """Save current cookies to file"""
        # if self.session and self.session.context and self.config.cookies_file:
        try:
            cookies = await self.session.context.cookies()
            logger.debug(f"Saving {len(cookies)} cookies to {self.config.cookies_file}")

            # Check if the path is a directory and create it if necessary
            # dirname = os.path.dirname(self.config.cookies_file)
            # if dirname:
            #     os.makedirs(dirname, exist_ok=True)

            # with open(self.config.cookies_file, "w") as f:
            #     json.dump(cookies, f)
        except Exception as e:
            logger.warning(f"Failed to save cookies: {str(e)}")


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
        # 配置备忘:
        # 1: channel=chrome 则使用了正式发行版(而不是chromium), 这样对于人机检测来说, 更不容易被识别为机器人
        # 2: 提示: 如果 browser_mode="builtin", 则chrome_channel和channel不会起作用
        # 3: 提示: 如果use_managed_browser=False, debugging_port= 这个参数不会打开cdp端口,但是可以额外的启动参数启动cdp端口,例如:
        #         extra_args=[f"--remote-debugging-port={settings.BROWSER_DEBUG_PORT}"]
        my_browser_config = config or BrowserConfig(
            browser_mode="dedicated",
            browser_type="chromium",
            chrome_channel="chrome",  # msedge
            channel="chrome",
            # use_managed_browser=True,
            headless=False,
            debugging_port=settings.BROWSER_DEBUG_PORT,
            # 提示: 如果use_managed_browser=False, debugging_port= 这个参数不会打开cdp端口,
            # 如果要打开cdp端口就额外添加启动参数
            extra_args=[f"--remote-debugging-port={settings.BROWSER_DEBUG_PORT}"],
            # use_persistent_context=True,  # 提示: 会强制 use_managed_browser = True
            cookies=[
                {
                    "name": "cookiesEnabled2222detector",
                    "value": "true",
                    "url": "https://bot-detector.rebrowser.net",
                    # if crawlerRunConfig
                    # else "https://crawl4ai.com/",
                }
            ],
        )
        super().__init__(
            crawler_strategy=crawler_strategy,
            config=my_browser_config,
            base_directory=base_directory,
            thread_safe=thread_safe,
            logger=logger,
        )

    async def get_playwright_browser_strategy(self):
        playwright_strategy = cast(
            AsyncPlaywrightCrawlerStrategy, self.crawler_strategy
        )
        # playwright_strategy.browser_manager.setup_context()
        return playwright_strategy

    async def get_browseruse_browser(self):
        # browser use 的浏览器通过 cdp 连接到 crawl4ai 的浏览器
        cdp_url = (
            self.browser_config.cdp_url
            if self.browser_config.cdp_url
            else f"http://{self.browser_config.host}:{self.browser_config.debugging_port}"
        )
        self.browseruse_browser = BrowserUseBrowser(
            config=MtBrowserConfig(
                headless=False,
                cdp_url=cdp_url,
            )
        )
        return self.browseruse_browser

    async def get_browseruse_context(self):
        browser_context = MtBrowseruseContext(
            browser=await self.get_browseruse_browser(),
            config=BrowserContextConfig(
                # user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36",
                # _force_keep_context_alive=True,
            ),
        )
        return browser_context
