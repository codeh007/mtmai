from browser_use.browser.context import BrowserContext
from loguru import logger
from playwright.async_api import Browser as PlaywrightBrowser
from playwright.async_api import Page


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
