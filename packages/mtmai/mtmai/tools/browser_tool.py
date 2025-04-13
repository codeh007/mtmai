from browser_use import Agent as BrowserUserAgent
from browser_use import Browser, BrowserConfig
from google.adk.tools import ToolContext
from langchain_google_genai import ChatGoogleGenerativeAI
from loguru import logger
from mtmai.core.config import settings
from mtmai.mtlibs.adk_utils.adk_utils import tool_success
from pydantic import SecretStr


def get_default_browser_config():
    browser = Browser(
        config=BrowserConfig(
            # headless=config.headless,
            headless=False,
            # browser_binary_path=config.chrome_path,
            # browser_binary_path=chrome_dir,
        )
    )
    return browser


async def browser_use_tool(task: str, tool_context: ToolContext) -> dict[str, str]:
    """基于 browser use 的浏览器自动化工具, 可以根据任务的描述,自动完成多个步骤的浏览器操作,并最终返回操作的结果.

    Args:
        task: 任务描述
        tool_context: ToolContext object.

    Returns:
        操作的最终结果
    """
    logger.info(f"browser_use_tool: {task}")

    browser = get_default_browser_config()
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.0-flash-exp",
        api_key=SecretStr(settings.GOOGLE_AI_STUDIO_API_KEY),
    )
    browser_user_agent = BrowserUserAgent(
        task=task,
        llm=llm,
        use_vision=False,
        browser=browser,
        max_actions_per_step=4,
    )

    result = await browser_user_agent.run(max_steps=25)
    return tool_success(result)
