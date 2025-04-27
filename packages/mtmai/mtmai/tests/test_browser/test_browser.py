import pytest
from browser_use import Agent as BrowseruseAgent
from browser_use import BrowserContextConfig
from browser_use.agent.views import AgentHistoryList
from browser_use.browser.context import BrowserContext as BrowseruseBrowserContext
from langchain_google_genai import ChatGoogleGenerativeAI
from mtmai.core.config import settings
from mtmai.mtlibs.browser_utils.browser_manager import BrowseruseHelper
from playwright.async_api import BrowserContext
from pydantic import SecretStr


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
async def test_browser1() -> None:
    # 这个不是正式的测试,可以删除.
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.0-flash-exp",
        api_key=SecretStr(settings.GOOGLE_AI_STUDIO_API_KEY),
    )

    helper = BrowseruseHelper()
    browser = await helper.get_browseruse_browser()
    browser_context = BrowseruseBrowserContext(
        browser=browser,
        config=BrowserContextConfig(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36",
        ),
    )
    async with browser_context as context:
        await setup_context(context.session.context)
        browser_user_agent = BrowseruseAgent(
            task="打开google 搜索美女相关的话题",
            llm=llm,
            use_vision=False,
            browser_context=context,
            # browser=browser,
            max_actions_per_step=4,
        )
        history: AgentHistoryList = await browser_user_agent.run(max_steps=25)
        print(history)
