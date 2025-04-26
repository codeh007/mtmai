import asyncio

from browser_use import Agent as BrowseruseAgent
from browser_use import BrowserContextConfig
from browser_use.agent.views import AgentHistoryList
from browser_use.browser.context import BrowserContext as BrowseruseBrowserContext
from crawl4ai.async_configs import BrowserConfig
from fastapi.encoders import jsonable_encoder
from google.adk.tools import ToolContext
from langchain_google_genai import ChatGoogleGenerativeAI
from loguru import logger
from mtmai.core.config import settings
from mtmai.mtlibs.adk_utils.adk_utils import tool_success
from mtmai.mtlibs.browser_utils.browser_manager import (
    BrowseruseHelper,
    MtBrowserManager,
)
from playwright.async_api import BrowserContext
from pydantic import SecretStr

STATE_KEY_BROWSER_CONFIG = "browser_config"
STATE_KEY_BROWSER_COOKIES = "browser_cookies"


def get_default_browser_config():
    BrowserConfig(
        browser_mode="dedicated",
        browser_type="chromium",
        chrome_channel="chrome",  # msedge
        channel="chrome",
        # use_managed_browser=True,
        headless=False,
        debugging_port=settings.BROWSER_DEBUG_PORT,
        # 提示: 如果use_managed_browser=False, debugging_port= 这个参数不会打开cdp端口,
        # 如果要打开cdp端口就额外添加启动参数
        extra_args=[f"--remote-debugging-port={settings.BROWSER_DEBUG_PORT}"],
        # use_persistent_context=True,  # 提示: 会强制 use_managed_browser = True
        cookies=[
            {
                "name": "cookiesEnabled2222detector",
                "value": "true",
                "url": "https://bot-detector.rebrowser.net",
                # if crawlerRunConfig
                # else "https://crawl4ai.com/",
            }
        ],
    )


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


# 通用任务
async def browser_use_tool(task: str, tool_context: ToolContext) -> dict[str, str]:
    """基于 browser use 的浏览器自动化工具, 可以根据任务的描述,自动完成多个步骤的浏览器操作,并最终返回操作的结果.

    Args:
        task: 任务描述
        tool_context: ToolContext object.

    Returns:
        操作的最终结果
    """
    logger.info(f"browser_use_tool: {task}")
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.0-flash-exp",
        api_key=SecretStr(settings.GOOGLE_AI_STUDIO_API_KEY),
    )

    # async with MtBrowserManager() as browser_manager:
    helper = BrowseruseHelper()
    browser = await helper.get_browseruse_browser()
    # async with await browser_manager.get_browseruse_context() as browseruse_context:
    # await setup_context(mtbrowseruse_context.session.context)

    # browser_context = await browser.new_context()
    browser_context = BrowseruseBrowserContext(
        browser=browser,
        config=BrowserContextConfig(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36",
        ),
    )
    async with browser_context as context:
        await setup_context(context.session.context)
        browser_user_agent = BrowseruseAgent(
            task=task,
            llm=llm,
            use_vision=False,
            browser_context=context,
            # browser=browser,
            max_actions_per_step=4,
        )
        # browser.playwright_browser.contexts

        # 提示: 仅返回最终的任务结果, 因此返回的结果太大会导致主线程的上下文过大
        #      其他有用信息保存到 state 即可
        history: AgentHistoryList = await browser_user_agent.run(max_steps=25)
        # browser_user_agent.
        tool_context.state.update({"browser_history": jsonable_encoder(history)})

    final_result = history.final_result()
    return tool_success(final_result)


# 创建独立的指纹环境
async def browser_use_steal_tool(tool_context: ToolContext) -> dict[str, str]:
    """创建浏览器指纹环境

    Args:
        tool_context: ToolContext object.

    Returns:
        操作的最终结果
    """
    browser_config = tool_context.state.get(
        STATE_KEY_BROWSER_CONFIG, get_default_browser_config()
    )
    async with MtBrowserManager(
        config=browser_config,
    ) as browser_manager:
        llm = ChatGoogleGenerativeAI(
            model="gemini-2.0-flash-exp",
            api_key=SecretStr(settings.GOOGLE_AI_STUDIO_API_KEY),
        )
        async with await browser_manager.get_browseruse_context() as browseruse_context:
            # 从 state 加载 cookies
            browser_cookies = tool_context.state.get(STATE_KEY_BROWSER_COOKIES, None)
            if browser_cookies:
                browseruse_context.session.context.add_cookies(browser_cookies)

            await setup_context(browseruse_context.session.context)

            steal_agent = BrowseruseAgent(
                # 其他 人机检测网站: https://bot.sannysoft.com/
                task="""
                    访问: https://bot-detector.rebrowser.net/ , 根据页面内容告我我是否已经通过了人机检测, 如果没有通过,具体原因是什么?
                """,
                llm=llm,
                browser_context=browseruse_context,
            )
            steal_history = await steal_agent.run(max_steps=5)

            # 保存相关 状态到 state
            cookies = await browseruse_context.session.context.cookies()
            tool_context.state.update(
                {STATE_KEY_BROWSER_COOKIES: jsonable_encoder(cookies)}
            )

        tool_context.state.update(
            {STATE_KEY_BROWSER_CONFIG: jsonable_encoder(browser_config)}
        )
        await asyncio.sleep(10)

        final_result = steal_history.final_result()
        return tool_success(final_result)


async def browser_human_interaction_tool(
    task: str, tool_context: ToolContext
) -> dict[str, str]:
    """网页操作过程中,遇到需要人工操作的场景, 可以调用这个工具, 工具会返回需要人工操作的场景, 并等待人工操作完成.

    Args:
        task: 需要人工具体的操作描述
        tool_context: ToolContext object.
    """
    logger.info("TODO: 现在智能体操作过程遇到需要人工操作的场景.")
    return tool_success("人工操作已经完成, 请继续后续任务.")
