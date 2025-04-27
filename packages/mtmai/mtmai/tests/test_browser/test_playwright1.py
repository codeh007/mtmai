import asyncio
import time

import pytest
from playwright.async_api import BrowserContext, async_playwright


async def setup_context(browseruse_context: BrowserContext):
    await browseruse_context.add_init_script(
        """
        console.log("hello world===============@ browser_use_tool")
        """
    )

    # 额外的反检测脚本
    async def load_undetect_script():
        undetect_script = open(
            "packages/mtmai/mtmai/mtlibs/browser_utils/stealth_js/undetect_script.js",
            "r",
        ).read()
        return undetect_script

    await browseruse_context.add_init_script(await load_undetect_script())

    await browseruse_context.add_cookies(
        [
            {
                "name": "cookiesExampleEnabled2222detector",
                "value": "true",
                "url": "https://bot-detector.rebrowser.net",
            }
        ]
    )
    # 添加 cookies(演示)
    await browseruse_context.add_cookies(
        [
            {
                "name": "cookiesExampleEnabled2222detector",
                "value": "true",
                "url": "https://bot-detector.rebrowser.net",
            }
        ]
    )


@pytest.mark.asyncio
async def test_playwright_browser1() -> None:
    # 方式1: 使用 playwright 的浏览器
    # async with async_playwright() as p:
    #     browser = await p.chromium.launch(
    #         headless=False,
    #         args=[
    #             "--disable-dev-shm-usage",
    #             "--no-first-run",
    #         ],
    #     )
    #     context = await browser.new_context()
    #     # await setup_context(context)
    #     page = await context.new_page()
    #     # Navigate to bing.com
    #     await page.goto("https://pixelscan.net/")
    #     # Wait for 10 seconds
    #     await asyncio.sleep(30)
    #     # Close browser
    #     await browser.close()
    # 方式2: 使用系统 Chrome 并添加反检测配置
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=False,
            executable_path="/opt/google/chrome/chrome",
            args=[
                "--disable-dev-shm-usage",
                "--no-first-run",
                "--no-default-browser-check",
                "--disable-infobars",
                "--window-position=0,0",
                "--disable-session-crashed-bubble",
                "--hide-crash-restore-bubble",
                "--disable-blink-features=AutomationControlled",
                "--disable-automation",
                "--disable-webgl",
                "--disable-webgl2",
                "--remote-debugging-port=15001",
            ],
        )

        context = await browser.new_context(
            viewport={"width": 1920, "height": 1080},
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            has_touch=True,
            is_mobile=False,
            color_scheme="light",
            locale="en-US",
            timezone_id="America/New_York",
        )

        # 添加反检测脚本
        await context.add_init_script("""
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined
            });
            Object.defineProperty(navigator, 'plugins', {
                get: () => [1, 2, 3, 4, 5]
            });
            window.chrome = {
                runtime: {}
            };
        """)

        page = await context.new_page()

        # 访问目标网站
        await page.goto("https://pixelscan.net/")

        # 等待30秒
        await asyncio.sleep(30)

        # 关闭浏览器
        await browser.close()


@pytest.mark.asyncio
async def test_playwright_browser2() -> None:
    """
    他进程已经启动了一个chrome 调试端口是: 15001
    """
    # 创建独立的 chrome prefile 并且打开 bing.com

    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp("http://localhost:15001")

        context = await browser.new_context()

        page = await context.new_page()
        await page.goto("https://bing.com")
        time.sleep(30)
