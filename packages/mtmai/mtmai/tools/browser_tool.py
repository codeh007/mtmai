from browser_use import Agent as BrowserUserAgent
from browser_use.agent.views import AgentHistoryList
from crawl4ai.async_configs import BrowserConfig
from fastapi.encoders import jsonable_encoder
from google.adk.tools import ToolContext
from langchain_google_genai import ChatGoogleGenerativeAI
from loguru import logger
from mtmai.core.config import settings
from mtmai.mtlibs.adk_utils.adk_utils import tool_success
from pydantic import SecretStr


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
    from crawl4ai.async_configs import BrowserConfig
    from mtmai.mtlibs.browser_utils.browser_manager import MtBrowserManager

    browser_manager = MtBrowserManager(
        browser_config=BrowserConfig(
            browser_type="chromium",
            chrome_channel="chrome",
            channel="chrome",
            headless=False,
            debugging_port=19222,
            use_managed_browser=True,
        )
    )
    await browser_manager.start()
    browser_context = await browser_manager.create_browser_use_context()

    llm = ChatGoogleGenerativeAI(
        model="gemini-2.0-flash-exp",
        api_key=SecretStr(settings.GOOGLE_AI_STUDIO_API_KEY),
    )

    steal_agent = BrowserUserAgent(
        task="""
            Go to https://bot-detector.rebrowser.net/ and verify that all the bot checks are passed.
        """,
        llm=llm,
        browser_context=browser_context,
    )
    stat_result = await steal_agent.run(max_steps=3)

    browser_user_agent = BrowserUserAgent(
        task=task,
        llm=llm,
        use_vision=False,
        browser_context=browser_context,
        max_actions_per_step=4,
    )

    # 提示: 仅返回最终的任务结果, 因此返回的结果太大会导致主线程的上下文过大
    #      其他有用信息保存到 state 即可
    history: AgentHistoryList = await browser_user_agent.run(max_steps=25)
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
    # from crawl4ai import BrowserConfig

    config = BrowserConfig(
        browser_type="chromium",
        headless=False,
        debugging_port=settings.BROWSER_DEBUG_PORT,
        use_managed_browser=True,
    )
    from mtmai.mtlibs.browser_utils.browser_manager import MtBrowserManager

    async with MtBrowserManager(config=config) as browser_manager:
        browser_context = await browser_manager.create_browser_use_context()
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
        # steal_agent = BrowserUserAgent(
        #     task="""
        #         访问: https://bot.sannysoft.com/ , 根据页面内容告我我是否已经通过了人机检测, 如果没有通过,具体原因是什么?
        #     """,
        #     llm=llm,
        #     browser_context=browser_context,
        # )

        steal_history = await steal_agent.run(max_steps=3)
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
