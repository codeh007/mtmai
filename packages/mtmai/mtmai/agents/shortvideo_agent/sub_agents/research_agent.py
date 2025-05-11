from textwrap import dedent

from google.adk.agents import LlmAgent
from google.genai import types  # noqa
from mtmai.model_client import get_default_litellm_model
from mtmai.tools.fetch_page import fetch_page_tool
from mtmai.tools.web_search import search_web_tool


def new_research_agent():
    research_agent = LlmAgent(
        name="research_agent",
        model=get_default_litellm_model(),
        description="""社交媒体话题调研专家""",
        instruction=dedent("""
你是专业的社交媒体话题调研专家，任务是根据用户给定的提示,输出话题的报告.

**工具**
* search_web_tool: 进行网络搜索
* fetch_page_tool: 获取网页内容

## Constrains:
1. 调研需要结合用户的意图.
2. 尽你最大的能力完成任务,不要向用户提问
3. 直接输出结果,不要解释,不要啰嗦.
4. 任务完成后, Transfer to root_agent


**提示**
- 当前日期: {current_date}
""").strip(),
        tools=[search_web_tool, fetch_page_tool],
        # after_agent_callback=after_agent_callback,
    )
    return research_agent
