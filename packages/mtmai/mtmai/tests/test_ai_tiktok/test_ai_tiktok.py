import asyncio

import pytest
from playwright.async_api import async_playwright


@pytest.mark.asyncio
async def test_playwright_browser2() -> None:
    # 创建独立的 chrome prefile 并且打开 bing.com
    # await get_ip_from_asock()

    # 第一步, 通过api 调用打开指纹浏览器

    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp("http://localhost:15001")

        # proxy_uri = parse_url(proxy_url)
        # proxy_uri = None
        context = await browser.new_context(
            timezone_id="Asia/Tokyo",
            locale="ja-JP",
            color_scheme="light",
            is_mobile=True,
            has_touch=True,
            viewport={"width": 1920, "height": 1080},
            user_agent="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
            # proxy={
            #     "server": f"{proxy_uri.scheme}://{proxy_uri.netloc}",
            #     "username": proxy_uri.auth.split(":")[0],
            #     "password": proxy_uri.auth.split(":")[1],
            # },
        )

        page = await context.new_page()

        await page.goto("https://bing.com")
        await page.wait_for_load_state("domcontentloaded")
        await asyncio.sleep(300)
