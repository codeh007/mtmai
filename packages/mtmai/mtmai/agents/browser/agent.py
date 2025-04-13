import os
from dataclasses import dataclass
from textwrap import dedent

from google.adk.agents import Agent
from mtmai.model_client.utils import get_default_litellm_model
from mtmai.tools.browser_tool import browser_use_tool


# ============ Configuration Section ============
@dataclass
class TwitterConfig:
    """Configuration for Twitter posting"""

    openai_api_key: str
    chrome_path: str
    target_user: str  # Twitter handle without @
    message: str
    reply_url: str
    headless: bool = False
    model: str = "gpt-4o-mini"
    base_url: str = "https://x.com/home"


# Customize these settings
config = TwitterConfig(
    openai_api_key=os.getenv("OPENAI_API_KEY"),
    chrome_path="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",  # This is for MacOS (Chrome)
    target_user="XXXXX",
    message="XXXXX",
    reply_url="XXXXX",
    headless=False,
)


def create_browser_agent():
    return Agent(
        model=get_default_litellm_model(),
        name="web_browser_agent",
        description="一个浏览器,可以浏览网页,获取网页内容,可以根据任务描述,自动浏览网页,获取网页内容,和模拟用户的操作,使用自主多步骤的流程,完成任务",
        instruction=dedent(
            """
            你是一个浏览器,可以浏览网页,获取网页内容,可以根据任务描述,自动浏览网页,获取网页内容,和模拟用户的操作,使用自主多步骤的流程,完成任务
            """
        ),
        tools=[browser_use_tool],
    )
