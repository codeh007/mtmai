from browser_use import Agent as BrowserUserAgent
from browser_use import (Browser, BrowserConfig, BrowserContextConfig,
                         Controller)
from browser_use.agent.views import AgentHistoryList
from browser_use.browser.context import BrowserContext, BrowserContextConfig
from fastapi.encoders import jsonable_encoder
from google.adk.tools import ToolContext
from langchain_google_genai import ChatGoogleGenerativeAI
from loguru import logger
from playwright._impl._api_structures import ProxySettings
from playwright.async_api import Browser as PlaywrightBrowser
from playwright.async_api import Route
from pydantic import SecretStr

from mtmai.core.config import settings
from mtmai.mtlibs.adk_utils.adk_utils import tool_success


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

    browser = await get_default_browser_config()
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.0-flash-exp",
        api_key=SecretStr(settings.GOOGLE_AI_STUDIO_API_KEY),
    )

    steal_agent = BrowserUserAgent(
        task="""
            Go to https://bot-detector.rebrowser.net/ and verify that all the bot checks are passed.
        """,
        llm=llm,
        browser=browser,
    )
    stat_result = await steal_agent.run(max_steps=3)

    browser_user_agent = BrowserUserAgent(
        task=task,
        llm=llm,
        use_vision=False,
        browser=browser,
        max_actions_per_step=4,
    )

    # 提示: 仅返回最终的任务结果, 因此返回的结果太大会导致主线程的上下文过大
    #      其他有用信息保存到 state 即可
    history: AgentHistoryList = await browser_user_agent.run(max_steps=25)
    tool_context.state.update({"browser_history": jsonable_encoder(history)})

    final_result = history.final_result()
    return tool_success(final_result)


controller = Controller()
# @controller.registry.action('Copy text to clipboard')
# def copy_to_clipboard(text: str):
# 	pyperclip.copy(text)
# 	return ActionResult(extracted_content=text)


# 创建独立的指纹环境
async def browser_use_steal_tool(tool_context: ToolContext) -> dict[str, str]:
    """创建浏览器指纹环境

    Args:
        tool_context: ToolContext object.

    Returns:
        操作的最终结果
    """
    # browser = get_default_browser_config()

    browser_context = await create_browser_context()

    # browser.playwright_browser.
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.0-flash-exp",
        api_key=SecretStr(settings.GOOGLE_AI_STUDIO_API_KEY),
    )

    steal_agent = BrowserUserAgent(
        task="""
            访问: https://bot-detector.rebrowser.net/ , 根据页面内容告我我是否已经通过了人机检测, 如果没有通过,具体原因是什么?
        """,
        llm=llm,
        browser_context=browser_context,
    )
    steal_history = await steal_agent.run(max_steps=3)

    # history: AgentHistoryList = await steal_agent.run(max_steps=25)
    tool_context.state.update(
        {
            "browser_config": jsonable_encoder(
                {
                    "hello": "value",
                }
            )
        }
    )

    final_result = steal_history.final_result()
    return tool_success(final_result)
    return tool_success(final_result)
