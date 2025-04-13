import urllib.request
from gettext import pgettext

from browser_use import Browser, BrowserConfig
from google.adk.tools import ToolContext
from mtmai.mtlibs.selenium_utils import get_chrome_path
from pydantic import BaseModel, Field
from loguru import logger


def get_default_browser_config():
    chrome_dir = get_chrome_path()
    browser = Browser(
        config=BrowserConfig(
            # headless=config.headless,
            headless=False,
            # browser_binary_path=config.chrome_path,
            browser_binary_path=chrome_dir,
        )
    )
    return browser


class BrowserUseInput(BaseModel):
    """Input for WriteFileTool."""

    instruction: str = Field(..., description="The instruction to use browser")
    #




def browser_use_tool(task: str, tool_context: ToolContext) -> dict[str, str]:
    """基于 browser use 的浏览器自动化工具, 可以根据任务的描述,自动完成多个步骤的浏览器操作,并最终返回操作的结果.

    Args:
        task: 任务描述
        tool_context: ToolContext object.

    Returns:
        操作的最终结果
    """
    logger.info(f"browser_use_tool: {task}")
    opener = urllib.request.build_opener()
    opener.addheaders = [("User-Agent", "Mozilla/5.0")]
    urllib.request.install_opener(opener)

    tool_context.state.update({"page_contents": pgettext})

    # tool_context.save_artifact(filename="page_contents.txt", artifact=page_text)
    return {"status": "OK"}
