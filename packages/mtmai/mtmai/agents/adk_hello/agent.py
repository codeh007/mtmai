from google.adk.agents import Agent
from google.adk.tools.agent_tool import AgentTool
from mtmai.agents.adk_hello.sub_agents.content_writer_agent import (
    new_content_writer_agent,
)
from mtmai.agents.adk_hello.sub_agents.extract_page_data_agent import (
    ExtractPageDataAgent,
)
from mtmai.agents.adk_hello.sub_agents.instagram_agent.instagram_agent import (
    new_instagram_agent,
)

# from mtmai.agents.adk_hello.sub_agents.topic_writer_agent import new_topic_writer_agent
from mtmai.model_client.utils import get_default_litellm_model
from mtmai.tools.fetch_page import fetch_page_tool

root_agent = Agent(
    name="webpage_summary_agent",
    model=get_default_litellm_model(),
    description=("根据用户的对话上下文,协助用户完成任务"),
    instruction=(
        """你是一个通用性助手,根据用户的对话上下文,协助用户完成任务
重要:
    你有多个合作伙伴,可以帮你分担特定方面的任务,你应该善于安排合适的任务给合作伙伴
    其中
    - topic_writer_agent擅长生成主题
    - content_writer_agent擅长生成内容
    - instagram_agent擅长操作 instagram 账户
    你需要主动判断任务是否正确完成,如果任务完成,请主动告诉用户任务完成
    应自己思考尽量完成任务,用户希望你尽可能自足完成任务, 不要总是咨询用户
"""
    ),
    sub_agents=[
        # new_topic_writer_agent(),
        new_content_writer_agent(),
        new_instagram_agent(),
    ],
    tools=[
        # 学习: fetch_page_tool + ExtractPageDataAgent 获取网页内容原代码 +
        # 智能提取所需的数据及格式放到聊天上下文中,
        # 进而后续的对话上下文中正确保存了所需的关键信息,同时又保留对话上下文的整洁
        # 而 html 源码保留在state 中, 可以后续根据具体需要二次用 ExtractPageDataAgent 再次提取
        # 更进一步,可以考虑使用 长期记忆(memory) + artifact 实现更加高级的功能.
        fetch_page_tool,
        AgentTool(ExtractPageDataAgent),
    ],
)
