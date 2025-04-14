from playwright._impl._api_structures import ProxySettings
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


# async def get_default_browser_config():
#     browser = Browser(
#         config=BrowserConfig(
#             headless=False,
#             proxy=proxy_url_to_proxy_setting(settings.default_proxy_url),
#             # browser_binary_path=chrome_dir,
#             disable_security=False,
#             _force_keep_browser_alive=True,
#             chrome_instance_path="/usr/bin/google-chrome",  # 使用google 正式版,有利于反扒检测
#             # new_context_config=BrowserContextConfig(
#             #     _force_keep_context_alive=True,
#             #     disable_security=False,
#             # ),
#             extra_chromium_args=["--user-data-dir=.vol/chrome_user_data"],
#         )
#     )

#     # browser = Browser(
#     #     config=BrowserConfig(
#     #         headless=False,
#     #         cdp_url="http://localhost:9222",
#     #     )
#     # )

#     return browser


# async def load_undetect_script():
#     undetect_script = open(
#         "packages/mtmai/mtmai/mtlibs/browser_utils/undetect_script.js", "r"
#     ).read()
#     return undetect_script


# class MtBrowserContext(BrowserContext):
#     # os.environ["DISPLAY"] = ":1"

#     async def _init(self):
#         if not hasattr(self, "browser_manager"):
#             self.browser_manager = MtBrowserManager(
#                 browser_config=MtBrowserConfig(
#                     browser_type="chromium",
#                     headless=False,
#                 )
#             )
#             await self.browser_manager.start()

#     async def _create_context(self, browser: PlaywrightBrowser):
#         await self._init()
#         playwright_context = await super()._create_context(browser)
#         from undetected_playwright import Malenia

#         await Malenia.apply_stealth(playwright_context)

#         # 额外的反检测脚本

#         await playwright_context.add_init_script(await load_undetect_script())

#         return playwright_context


# async def create_browser_context():
#     # 指纹
#     # 参考: https://github.com/QIN2DIM/undetected-playwright?tab=readme-ov-file

#     # browser = await get_default_browser_config()

#     browser_context = MtBrowserContext(
#         config=BrowserContextConfig(
#             disable_security=False,  # 如果禁用了 csp, 一般会被识别为机器人
#             user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36",
#         ),
#         browser=browser,
#     )

#     # playwright_session = await browser_context.get_session()
#     # await Malenia.apply_stealth(playwright_session.context)
#     return browser_context


# controller = Controller()
# @controller.registry.action('Copy text to clipboard')
# def copy_to_clipboard(text: str):
# 	pyperclip.copy(text)
# 	return ActionResult(extracted_content=text)
