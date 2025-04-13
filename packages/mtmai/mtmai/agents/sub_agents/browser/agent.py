import os
from dataclasses import dataclass

from browser_use import Agent as BrowserAgent
from browser_use.browser.browser import Browser, BrowserConfig
from browser_use.controller.service import Controller
from google.adk.agents import Agent
from langchain_google_genai import ChatGoogleGenerativeAI
from mtmai.core.config import settings
from mtmai.model_client.utils import get_default_litellm_model
from pydantic import SecretStr

CONTENT_WRITER_AGENT_PROMPT = """
你是擅长内容创作的专家,根据用户给定的主题,生成文章的正文
"""


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
    browser = Browser(
        config=BrowserConfig(
            headless=config.headless,
            browser_binary_path=config.chrome_path,
        )
    )
    controller = Controller()
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.0-flash-exp",
        api_key=SecretStr(settings.GOOGLE_AI_STUDIO_API_KEY),
    )
    browser_user_agent = BrowserAgent(
        task="打开必应搜索引擎,搜索随便一个酒类相关的内容",
        llm=llm,
        use_vision=False,
        browser=browser,
        max_actions_per_step=4,
    )

    return Agent(
        model=get_default_litellm_model(),
        name="web_browser_agent",
        description="一个浏览器,可以浏览网页,获取网页内容,可以根据任务描述,自动浏览网页,获取网页内容,和模拟用户的操作,使用自主多步骤的流程,完成任务",
        instruction=CONTENT_WRITER_AGENT_PROMPT,
        tools=[],
    )
