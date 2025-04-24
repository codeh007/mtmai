from autogen_core import tool_agent
from google.adk.agents import Agent
from google.adk.agents.callback_context import CallbackContext
from loguru import logger

# from mtmai.crawl4ai.async_configs import BrowserConfig  # noqa: F401
from mtmai.agents.root.prompt import return_instructions_root
from mtmai.model_client.utils import get_default_litellm_model
from pydantic import BaseModel

# from mtmai.agents.adk_smolagent.adk_smolagent import (
#     # adk_smolagent_browser_automation_tool,
# )  # noqa: F401
# from mtmai.agents.open_deep_research.open_deep_research import (
#     adk_open_deep_research_tool,
# )


class HelloState1(BaseModel):
    hello: str


def before_agent_callback(callback_context: CallbackContext):
    logger.info("before_agent_callback ")
    callback_context.state["root_agent_init123"] = "root_agent_init456"
    callback_context.state["hello_state1"] = HelloState1(hello="world").model_dump()


def get_agent_by_name(name: str) -> Agent:
    if name == "webpage_summary_agent":
        return tool_agent
    elif name == "instagram_agent":
        from mtmai.agents.sub_agents.instagram_agent.instagram_agent import (
            new_instagram_agent,
        )

        return new_instagram_agent()
    elif name == "content_writer_agent":
        from mtmai.agents.sub_agents.content_writer_agent import (
            new_content_writer_agent,
        )

        return new_content_writer_agent()
    elif name == "browser_agent":
        # return new_search_results_agent()
        from mtmai.agents.browser.browser_agent import create_browser_agent

        return create_browser_agent()
    elif name == "browser_automation_agent":
        from mtmai.agents.adk_smolagent.adk_smolagent import create_adk_smolagent

        return create_adk_smolagent()
    else:
        raise ValueError(f"agent {name} not found")


root_agent = Agent(
    name="root_agent",
    model=get_default_litellm_model(),
    description=("根据用户的对话上下文,协助用户完成任务"),
    instruction=return_instructions_root(),
    sub_agents=[
        # get_agent_by_name("content_writer_agent"),
        # get_agent_by_name("instagram_agent"),
        # get_agent_by_name("browser_agent"),
        # get_agent_by_name("browser_automation_agent"),
        #         WriterAgent(
        #             name="writer_agent",
        #             model=get_default_litellm_model(),
        #             description="专业的博客文章撰写助手",
        #             instruction=(
        #                 """你是专业的博客文章撰写助手, 根据用户的需求, 撰写博客文章.
        # 重要:
        #     文章应该包含标题和正文.
        #     语气应该是调皮的, 轻松的, 有趣的.
        # """
        #             ),
        #         ),
    ],
    before_agent_callback=before_agent_callback,
    tools=[
        # adk_smolagent_browser_automation_tool
        # adk_smolagent_blogwriter_tool,
        # adk_open_deep_research_tool,
        # 学习: fetch_page_tool + ExtractPageDataAgent 获取网页内容原代码 +
        # 智能提取所需的数据及格式放到聊天上下文中,
        # 进而后续的对话上下文中正确保存了所需的关键信息,同时又保留对话上下文的整洁
        # 而 html 源码保留在state 中, 可以后续根据具体需要二次用 ExtractPageDataAgent 再次提取
        # 更进一步,可以考虑使用 长期记忆(memory) + artifact 实现更加高级的功能.
        # fetch_page_tool,
        # AgentTool(ExtractPageDataAgent),
    ],
)
