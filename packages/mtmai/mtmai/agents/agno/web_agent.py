import json

import httpx
from phi.agent import Agent
from phi.tools.duckduckgo import DuckDuckGo

from mtmai.agents.phiagents.config import model
from mtmai.core.logging import get_logger

logger = get_logger()


def get_site_id() -> str:
    """获取当前用户的siteId.

    Args:
        no args required

    Returns:
        str: siteId.
    """

    return "site-12345"


web_agent = Agent(
    name="Web Agent",
    role="Search the web for information",
    model=model,
    tools=[get_site_id],
    markdown=True,
    show_tool_calls=True,
)
