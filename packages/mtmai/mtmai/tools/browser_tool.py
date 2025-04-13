from browser_use import Agent as BrowserUserAgent
from browser_use import Browser, BrowserConfig, BrowserContextConfig
from browser_use.agent.views import AgentHistoryList
from fastapi.encoders import jsonable_encoder
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
            # keep_alive=True,
            # browser_binary_path=config.chrome_path,
            # browser_binary_path=chrome_dir,
            disable_security=True,
            _force_keep_browser_alive=True,
            new_context_config=BrowserContextConfig(
                _force_keep_context_alive=True,
                disable_security=False,
            ),
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

    # 提示: 仅返回最终的任务结果, 因此返回的结果太大会导致主线程的上下文过大
    #      其他有用信息保存到 state 即可
    history: AgentHistoryList = await browser_user_agent.run(max_steps=25)
    tool_context.state.update({"browser_history": jsonable_encoder(history)})

    final_result = history.final_result()
    return tool_success(final_result)
