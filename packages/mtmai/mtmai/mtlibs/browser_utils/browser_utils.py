from browser_use import Browser, BrowserConfig, BrowserContextConfig, Controller
from browser_use.browser.context import BrowserContext
from mtmai.core.config import settings
from playwright._impl._api_structures import ProxySettings
from playwright.async_api import Browser as PlaywrightBrowser
from playwright.async_api import Route


def proxy_url_to_proxy_setting(proxy_url: str) -> ProxySettings:
    """Convert a proxy URL string to ProxySettings structure.

    Args:
        proxy_url: Proxy URL in format 'http://username:password@host:port'

    Returns:
        ProxySettings object with server, username and password fields
    """
    from urllib.parse import urlparse

    parsed = urlparse(proxy_url)
    settings = ProxySettings()

    # Build server string
    server = f"{parsed.hostname}:{parsed.port}"
    settings["server"] = server

    # Extract credentials if present
    if parsed.username:
        settings["username"] = parsed.username
    if parsed.password:
        settings["password"] = parsed.password

    return settings


async def _hijacker(route: Route):
    # logging.debug(f"{route.request.method} {route.request.url}")
    await route.continue_()


async def get_default_browser_config():
    browser = Browser(
        config=BrowserConfig(
            headless=False,
            proxy=proxy_url_to_proxy_setting(settings.default_proxy_url),
            # browser_binary_path=chrome_dir,
            disable_security=False,
            _force_keep_browser_alive=True,
            # new_context_config=BrowserContextConfig(
            #     _force_keep_context_alive=True,
            #     disable_security=False,
            # ),
        )
    )

    # browser = Browser(
    #     config=BrowserConfig(
    #         headless=False,
    #         cdp_url="http://localhost:9222",
    #     )
    # )

    return browser


undetect_script = """
console.log("设置额外的 反检测脚本");
navigator.webdriver = false;
window.__pwInitScripts=undefined;
navigator.userAgentData = {
    "brands": [
        {
            "brand": "Google Chrome",
            "version": "135"
        },
        {
            "brand": "Not-A.Brand",
            "version": "8"
        },
        {
            "brand": "Chromium",
            "version": "135"
        }
    ],
    "mobile": false,
    "platform": "Windows"
}

console.log("设置额外的 反检测脚本结束");

"""


class MtBrowserContext(BrowserContext):
    async def _create_context(self, browser: PlaywrightBrowser):
        playwright_context = await super()._create_context(browser)
        from undetected_playwright import Malenia

        await Malenia.apply_stealth(playwright_context)

        # 额外的反检测脚本

        await playwright_context.add_init_script(undetect_script)

        return playwright_context


async def create_browser_context():
    # 指纹
    # 参考: https://github.com/QIN2DIM/undetected-playwright?tab=readme-ov-file
    browser = await get_default_browser_config()

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


controller = Controller()
# @controller.registry.action('Copy text to clipboard')
# def copy_to_clipboard(text: str):
# 	pyperclip.copy(text)
# 	return ActionResult(extracted_content=text)
