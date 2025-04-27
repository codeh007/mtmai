import asyncio

import httpx
import pytest
from playwright.async_api import BrowserContext, async_playwright
from urllib3.util import parse_url

proxy_url = "http://mcj4hubox7-corp.mobile.res-country-JP-state-2112518-city-1907265-hold-hardsession-session-680e05c4abb26:2djXEAgx15LyN8pg@109.236.82.42:9999"


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


async def get_ip_from_asock():
    api_key = "MI1hffVbptDPIC1Rs4ray2PTDIt3g73F"
    blance_url = f"https://api.asocks.com/v2/user/balance?apiKey={api_key}"

    async with httpx.AsyncClient() as httpclient:
        response = await httpclient.get(
            blance_url, headers={"Authorization": f"Bearer {api_key}"}
        )
        response_text = response.text
        print(response_text)

    postData = {
        "country_code": "US",
        "state": "New York",
        "city": "New York",
        "asn": 11,
        "type_id": 1,
        "proxy_type_id": 2,
        "name": None,
        "server_port_type_id": 1,
        "count": 1,
        "ttl": 1,
    }
    async with httpx.AsyncClient() as httpclient:
        url2 = f"https://api.asocks.com/v2/proxy/create-port?apiKey={api_key}"
        response = await httpclient.post(
            url2,
            json=postData,
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
            },
        )
        response_text = response.text
        print(response_text)


@pytest.mark.asyncio
async def test_playwright_browser2() -> None:
    """
    进程已经启动了一个chrome 调试端口是: 15001
    """
    # 创建独立的 chrome prefile 并且打开 bing.com
    await get_ip_from_asock()
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp("http://localhost:15001")

        proxy_uri = parse_url(proxy_url)
        context = await browser.new_context(
            timezone_id="Asia/Tokyo",
            locale="ja-JP",
            color_scheme="light",
            is_mobile=True,
            has_touch=True,
            viewport={"width": 1920, "height": 1080},
            user_agent="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
            proxy={
                "server": f"{proxy_uri.scheme}://{proxy_uri.netloc}",
                "username": proxy_uri.auth.split(":")[0],
                "password": proxy_uri.auth.split(":")[1],
            },
        )

        page = await context.new_page()

        await page.goto("https://bing.com")
        await page.wait_for_load_state("domcontentloaded")
        await asyncio.sleep(300)
