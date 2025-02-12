import logging

from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.conditions import MaxMessageTermination, TextMentionTermination
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_core.tools import FunctionTool
from mtmaisdk.clients.rest.models.model_config import ModelConfig

from mtmai.tools.calculator import web_search

from mtmai.agents._agents import MtRoundRobinGroupChat
from ..model_client import MtmOpenAIChatCompletionClient, get_oai_Model

logger = logging.getLogger(__name__)


class TravelTeamBuilder:
    """Manages team operations including loading configs and running teams"""

    # def create_runner_by_name(self, name: str):
    #     """根据名称创建runner"""
    #     if name == "demo_team":
    #         return self.create_demo_team()
    #     elif name == "demo_agent_stream1":
    #         return self.create_demo_agent_stream1()

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

    async def create_travel_agent(self, model_config: ModelConfig):
        """创建旅行助理"""

        model_dict = model_config.model_dump()
        model_dict["model_info"] = model_dict.pop("model_info", None)
        model_dict.pop("n", None)
        model_client = MtmOpenAIChatCompletionClient(
            **model_dict,

        )

        # 提示: participants 中,不能也不应添加 UserProxyAgent
        # user_proxy_agent = MtWebUserProxyAgent(
        #     name="web_user",
        # )
        planner_agent = AssistantAgent(
            name="planner_agent",
            model_client=model_client,
            description="A helpful assistant that can plan trips.",
            system_message="You are a helpful assistant that can suggest a travel plan for a user based on their request.",
        )

        local_agent = AssistantAgent(
            name="local_agent",
            model_client=model_client,
            description="A local assistant that can suggest local activities or places to visit.",
            system_message="You are a helpful assistant that can suggest authentic and interesting local activities or places to visit for a user and can utilize any context information provided.",
        )

        language_agent = AssistantAgent(
            name="language_agent",
            model_client=model_client,
            description="A helpful assistant that can provide language tips for a given destination.",
            system_message="You are a helpful assistant that can review travel plans, providing feedback on important/critical tips about how best to address language or communication challenges for the given destination. If the plan already includes language tips, you can mention that the plan is satisfactory, with rationale.",
        )

        travel_summary_agent = AssistantAgent(
            name="travel_summary_agent",
            model_client=model_client,
            description="A helpful assistant that can summarize the travel plan.",
            system_message="You are a helpful assistant that can take in all of the suggestions and advice from the other agents and provide a detailed final travel plan. You must ensure that the final plan is integrated and complete. YOUR FINAL RESPONSE MUST BE THE COMPLETE PLAN. When the plan is complete and all perspectives are integrated, you can respond with TERMINATE.",
        )

        termination = TextMentionTermination(text="TERMINATE")
        max_msg_termination = MaxMessageTermination(max_messages=5)
        combined_termination = max_msg_termination & termination
        team = MtRoundRobinGroupChat(
            participants=[
                # user_proxy_agent,
                planner_agent,
                local_agent,
                language_agent,
                travel_summary_agent,
            ],
            termination_condition=combined_termination,
        )
        team.component_version = 2
        team.component_label = "travel_agent"
        team.component_description = "行程规划团队"
        return team
