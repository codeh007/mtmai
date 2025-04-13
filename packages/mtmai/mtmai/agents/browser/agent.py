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
        description="网页浏览器操作助理,可以根据任务描述,自动浏览网页,获取网页内容,和模拟用户的操作,使用自主多步骤的流程,完成任务",
        instruction=dedent(
            """你是专业操作浏览器的助手,擅长根据用户的对话上下文调用工具完成用户的指定任务.
重要:
    - 工具是开源 browser use, 版本号是 v0.1.40, 你必须一次性通过自然语音的描述将完整的任务交代清楚,
    - browser use 本身是 ai agent 可以理解你的任务并且内部能智能规划通过多个步骤操作浏览器来完成你给出的任务.
    - browser use 在任务结束后给你返回任务的最终结果描述, 并且会将任务的相关状态保存. 你可以在下一轮对话中获取到任务的结果的详细描述以及关键状态数据
    - 如果任务需要一些基本的资料, 你应该再任务描述中附带, 特别是 账号, 网址, 等等.
    - 你需要完全明白浏览器所需的任务规划, 给出经过优化的步骤规划指引 browser use 操作
    - 你需要完全了解用户的意图以及任务涉及网站的相关特性

"""
        ),
        tools=[browser_use_tool],
    )
