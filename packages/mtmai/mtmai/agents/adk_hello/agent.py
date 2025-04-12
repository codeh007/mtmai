from google.adk.agents import Agent
from mtmai.agents.adk_hello.sub_agents.content_writer_agent import (
    new_content_writer_agent,
)
from mtmai.agents.adk_hello.sub_agents.topic_writer_agent import new_topic_writer_agent
from mtmai.model_client.utils import get_default_litellm_model
from mtmai.tools.fetch_page import fetch_page_tool
from mtmai.tools.store_state import store_state_tool

root_agent = Agent(
    name="webpage_summary_agent",
    model=get_default_litellm_model(),
    description=("根据用户的对话上下文,协助用户完成任务"),
    instruction=(
        """你是一个通用性助手,根据用户的对话上下文,协助用户完成任务
重要:
    你有两个合作助理,可以帮你分担特定方面的任务,你应该善于安排合适的任务给合作助理
    其中topic_writer_agent擅长生成主题,content_writer_agent擅长生成内容
    你需要主动判断任务是否正确完成,如果任务完成,请主动告诉用户任务完成
    不到迫不得已, 应自己思考尽量完成任务,二不要想用户咨询各种选择
"""
    ),
    sub_agents=[new_topic_writer_agent(), new_content_writer_agent()],
    tools=[fetch_page_tool, store_state_tool],
)
