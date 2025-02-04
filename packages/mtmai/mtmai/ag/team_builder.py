import logging

from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.conditions import MaxMessageTermination, TextMentionTermination
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_core.tools import FunctionTool

from ..tools.calculator import web_search
from .model_client import get_oai_Model

logger = logging.getLogger(__name__)


class TeamBuilder:
    """Manages team operations including loading configs and running teams"""

    def create_runner_by_name(self, name: str):
        """根据名称创建runner"""
        if name == "demo_team":
            return self.create_demo_team()
        elif name == "demo_agent_stream1":
            return self.create_demo_agent_stream1()

    async def create_demo_team(self):
        """创建默认测试团队"""
        base_model = get_oai_Model()
        calculator_fn_tool = FunctionTool(
            name="calculator",
            description="A simple calculator that performs basic arithmetic operations",
            func=web_search,
            global_imports=[],
        )

        calc_assistant = AssistantAgent(
            name="assistant_agent",
            system_message="You are a helpful assistant. Solve tasks carefully. When done, say TERMINATE.",
            model_client=base_model,
            tools=[calculator_fn_tool],
        )
        # Create termination conditions for calculator team
        calc_text_term = TextMentionTermination(text="TERMINATE")
        calc_max_term = MaxMessageTermination(max_messages=10)
        calc_or_term = calc_text_term | calc_max_term
        calc_or_term = calc_text_term | calc_max_term
        calc_team = RoundRobinGroupChat(
            participants=[calc_assistant], termination_condition=calc_or_term
        )
        return calc_team

    async def create_demo_agent_stream1(self):
        """试试流式token"""
        assistant = AssistantAgent(
            name="assistant",
            # tools=[get_weather],
            model_client=get_oai_Model(),
            system_message="You are a helpful assistant",
            # 提示: 流式token 需要设置 model_client_stream=True
            #       设置后,可以使用 run_stream 中获取流式token
            #       对应的事件类型是: ModelClientStreamingChunkEvent
            model_client_stream=True,
            reflect_on_tool_use=True,  # Reflect on tool use.
        )
        return assistant
