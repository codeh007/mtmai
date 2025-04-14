import os

from browser_use import Browser, BrowserConfig, BrowserContextConfig

# from mtmai. import MtBrowserContext
from browser_use.browser.context import BrowserContext
from mtmai.crawl4ai.browser_manager import BrowserManager
from mtmai.mtlibs.browser_utils.browser_config import MtBrowserConfig
from playwright.async_api import Browser as PlaywrightBrowser


class MtBrowserContext(BrowserContext):
    # os.environ["DISPLAY"] = ":1"

    async def _init(self):
        if not hasattr(self, "browser_manager"):
            self.browser_manager = MtBrowserManager(
                browser_config=MtBrowserConfig(
                    browser_type="chromium",
                    headless=False,
                )
            )
            await self.browser_manager.start()

    async def _create_context(self, browser: PlaywrightBrowser):
        await self._init()
        playwright_context = await super()._create_context(browser)
        from undetected_playwright import Malenia

        await Malenia.apply_stealth(playwright_context)

        # 额外的反检测脚本

        # await playwright_context.add_init_script(await load_undetect_script())

        return playwright_context


class MtBrowserManager(BrowserManager):
    # def __init__(self, browser_type: str = "chromium", headless: bool = True):
    #     self.browser_type = browser_type
    #     self.headless = headless

    async def start(self):
        os.environ["DISPLAY"] = ":1"
        await super().start()

    async def create_browser_use_context():
        # 指纹
        # 参考: https://github.com/QIN2DIM/undetected-playwright?tab=readme-ov-file

        # browser = await get_default_browser_config()

        browser = Browser(
            config=BrowserConfig(
                headless=False,
                cdp_url="http://localhost:9222",
            )
        )

        browser_context = MtBrowserContext(
            config=BrowserContextConfig(
                disable_security=False,  # 如果禁用了 csp, 一般会被识别为机器人
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36",
            ),
            browser=browser,
        )

        # playwright_session = await browser_context.get_session()
        # await Malenia.apply_stealth(playwright_session.context)
        return browser_context
