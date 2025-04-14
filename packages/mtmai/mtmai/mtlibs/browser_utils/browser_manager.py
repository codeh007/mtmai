import os

from browser_use import Browser as BrowserUseBrowser
from browser_use import BrowserConfig, BrowserContextConfig
from browser_use.browser.context import BrowserContext
from loguru import logger
from mtmai.crawl4ai.browser_manager import BrowserManager
from mtmai.mtlibs.browser_utils.browser_config import MtBrowserConfig
from playwright.async_api import Browser as PlaywrightBrowser
from playwright.async_api import Page
from playwright_stealth.core import StealthConfig


async def load_undetect_script():
    undetect_script = open(
        "packages/mtmai/mtmai/mtlibs/browser_utils/stealth_js/undetect_script.js", "r"
    ).read()
    return undetect_script


stealth_config = StealthConfig(
    webdriver=True,
    chrome_app=True,
    chrome_csi=True,
    chrome_load_times=True,
    chrome_runtime=True,
    navigator_languages=True,
    navigator_plugins=True,
    navigator_permissions=True,
    webgl_vendor=True,
    outerdimensions=True,
    navigator_hardware_concurrency=True,
    media_codecs=True,
)


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

        # properties = Properties(browser_type=stealth_config.browser_type if stealth_config else BrowserType.CHROME)
        # combined_script = combine_scripts(properties, stealth_config)
        # await generate_stealth_headers_async(properties, page)

        # await page.add_init_script(combined_script)
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
        # await stealth_async(page)


class MtBrowserManager(BrowserManager):
    async def start(self):
        os.environ["DISPLAY"] = ":1"
        await super().start()

    async def create_browser_use_context(self):
        # 指纹
        # 参考: https://github.com/QIN2DIM/undetected-playwright?tab=readme-ov-file

        # browser = await get_default_browser_config()

        # c=await self.browser.new_context()

        # managed_browser = ManagedBrowser(
        #     browser_type="chromium",
        #     headless=False,
        #     debugging_port=19222,
        # )
        # cdp_url = await managed_browser.start()

        # aa= await self.create_browser_context()
        # default_context = self.default_context

        browser = BrowserUseBrowser(
            config=BrowserConfig(
                headless=False,
                disable_security=False,
                cdp_url=f"http://{self.config.host}:{self.config.debugging_port}",
                # cdp_url=self.,
            )
        )

        browser_context = MtBrowserContext(
            config=BrowserContextConfig(
                disable_security=False,  # 如果禁用了 csp, 一般会被识别为机器人
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36",
            ),
            browser=browser,
        )
        return browser_context
