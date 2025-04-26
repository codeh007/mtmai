from browser_use import BrowserConfig as BrowseruseBrowserConfig  # noqa
from browser_use import BrowserContextConfig
from browser_use.browser.context import BrowserContext as BrowseruseBrowserContext  # noqa

# from mtmai.crawl4ai.async_configs import BrowserConfig
# from mtmai.crawl4ai.async_crawler_strategy import (
#     AsyncCrawlerStrategy,
#     AsyncPlaywrightCrawlerStrategy,
# )
# from mtmai.crawl4ai.async_webcrawler import AsyncWebCrawler
# from mtmai.crawl4ai.types import AsyncLoggerBase


class BrowseruseHelper:
    async def get_browseruse_browser(self):
        # 方式1: browser use 的浏览器通过 cdp 连接到 crawl4ai 的浏览器
        from browser_use import Browser as BrowserUseBrowser  # noqa

        # cdp_url = (
        #     self.browser_config.cdp_url
        #     if self.browser_config.cdp_url
        #     else f"http://{self.browser_config.host}:{self.browser_config.debugging_port}"
        # )
        # self.browseruse_browser = BrowserUseBrowser(
        #     config=BrowseruseBrowserConfig(
        #         headless=False,
        #         cdp_url=cdp_url,
        #     )
        # )
        # 方式2: browseruse 自托管
        browseruse_browser = BrowserUseBrowser(
            config=BrowseruseBrowserConfig(
                headless=False,
                disable_security=False,
                chrome_instance_path="/opt/google/chrome/chrome",
                extra_chromium_args=[
                    "--disable-dev-shm-usage",
                    "--no-first-run",
                    "--no-default-browser-check",
                    "--disable-infobars",
                    "--window-position=0,0",
                    "--disable-session-crashed-bubble",  # 关闭崩溃提示
                    "--hide-crash-restore-bubble",  # 关闭崩溃恢复提示
                ],
                new_context_config=BrowserContextConfig(
                    user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36",
                ),
            )
        )
        return browseruse_browser


# class MtBrowserManager(AsyncWebCrawler):
#     """
#     设计备忘:
#         1: crawl4ai 的 AsyncWebCrawler 设计比较合理, 因此这里跟浏览器相关的上下文直接复用这个类
#         2: 增加功能: 让 browser use 的浏览器上下文共享 crawl4ai 的浏览器上下文
#     """

#     def __init__(
#         self,
#         crawler_strategy: AsyncCrawlerStrategy = None,
#         config: BrowserConfig = None,
#         base_directory: str = str(os.getenv("CRAWL4_AI_BASE_DIRECTORY", Path.home())),
#         thread_safe: bool = False,
#         logger: AsyncLoggerBase = None,
#         **kwargs,
#     ):
#         # 配置备忘:
#         # 1: channel=chrome 则使用了正式发行版(而不是chromium), 这样对于人机检测来说, 更不容易被识别为机器人
#         # 2: 提示: 如果 browser_mode="builtin", 则chrome_channel和channel不会起作用
#         # 3: 提示: 如果use_managed_browser=False, debugging_port= 这个参数不会打开cdp端口,但是可以额外的启动参数启动cdp端口,例如:
#         #         extra_args=[f"--remote-debugging-port={settings.BROWSER_DEBUG_PORT}"]
#         my_browser_config = config or BrowserConfig(
#             browser_mode="dedicated",
#             browser_type="chromium",
#             chrome_channel="chrome",  # msedge
#             channel="chrome",
#             # use_managed_browser=True,
#             headless=False,
#             debugging_port=settings.BROWSER_DEBUG_PORT,
#             # 提示: 如果use_managed_browser=False, debugging_port= 这个参数不会打开cdp端口,
#             # 如果要打开cdp端口就额外添加启动参数
#             extra_args=[f"--remote-debugging-port={settings.BROWSER_DEBUG_PORT}"],
#             # use_persistent_context=True,  # 提示: 会强制 use_managed_browser = True
#             cookies=[
#                 {
#                     "name": "cookiesEnabled2222detector",
#                     "value": "true",
#                     "url": "https://bot-detector.rebrowser.net",
#                     # if crawlerRunConfig
#                     # else "https://crawl4ai.com/",
#                 }
#             ],
#         )
#         super().__init__(
#             crawler_strategy=crawler_strategy,
#             config=my_browser_config,
#             base_directory=base_directory,
#             thread_safe=thread_safe,
#             logger=logger,
#         )

#     async def get_playwright_browser_strategy(self):
#         playwright_strategy = cast(
#             AsyncPlaywrightCrawlerStrategy, self.crawler_strategy
#         )
#         # playwright_strategy.browser_manager.setup_context()
#         return playwright_strategy

#     # async def get_browseruse_browser(self):
#     #     # 方式1: browser use 的浏览器通过 cdp 连接到 crawl4ai 的浏览器
#     #     from browser_use import Browser as BrowserUseBrowser  # noqa

#     #     # cdp_url = (
#     #     #     self.browser_config.cdp_url
#     #     #     if self.browser_config.cdp_url
#     #     #     else f"http://{self.browser_config.host}:{self.browser_config.debugging_port}"
#     #     # )
#     #     # self.browseruse_browser = BrowserUseBrowser(
#     #     #     config=BrowseruseBrowserConfig(
#     #     #         headless=False,
#     #     #         cdp_url=cdp_url,
#     #     #     )
#     #     # )
#     #     # 方式2: browseruse 自托管
#     #     browseruse_browser = BrowserUseBrowser(
#     #         config=BrowseruseBrowserConfig(
#     #             headless=False,
#     #             disable_security=False,
#     #             chrome_instance_path="/opt/google/chrome/chrome",
#     #             extra_chromium_args=[
#     #                 "--disable-dev-shm-usage",
#     #                 "--no-first-run",
#     #                 "--no-default-browser-check",
#     #                 "--disable-infobars",
#     #                 "--window-position=0,0",
#     #                 "--disable-session-crashed-bubble",  # 关闭崩溃提示
#     #                 "--hide-crash-restore-bubble",  # 关闭崩溃恢复提示
#     #             ],
#     #             new_context_config=BrowserContextConfig(
#     #                 user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36",
#     #             ),
#     #         )
#     #     )
#     #     return browseruse_browser

#     # async def get_browseruse_context(self):
#     #     browser_context = BrowseruseBrowserContext(
#     #         browser=await self.get_browseruse_browser(),
#     #         config=BrowserContextConfig(
#     #             # user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36",
#     #             # _force_keep_context_alive=True,
#     #         ),
#     #     )
#     #     return browser_context
