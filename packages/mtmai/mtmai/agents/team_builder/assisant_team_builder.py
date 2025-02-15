import logging

from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.conditions import MaxMessageTermination, TextMentionTermination
from autogen_agentchat.teams import RoundRobinGroupChat
# from ...gomtm_client import get_gomtm_client
from mtmaisdk.clients.rest.models.model_config import ModelConfig
from ...mtmaisdk.clients.rest_client import AsyncRestApi

from ..model_client import MtmOpenAIChatCompletionClient

logger = logging.getLogger(__name__)

class AssistantTeamBuilder:
    """默认聊天团队"""
    def __init__(self):
        # self.gomtmapi = get_gomtm_client()
        pass

    async def create_team(self):
        model_client = MtmOpenAIChatCompletionClient(
            model="tenant_default",
        )
        planner_agent = AssistantAgent(
            name="planner_agent",
            model_client=model_client,
            description="足球赛事分析",
            system_message="你是足球赛事分析专家，可以分析足球赛事，并给出分析结果",
        )
        language_agent = AssistantAgent(
            name="投注建议专家",
            model_client=model_client,
            description="投注建议专家，可以给出投注建议",
            system_message="你是投注建议专家，可以给出投注建议",
        )

        summary_agent = AssistantAgent(
            name="足彩助理",
            model_client=model_client,
            description="足彩助理，可以给出足彩投注建议",
            system_message="你是足彩助理，可以给出足彩投注建议,当你有确定答案时，你可以输出 TERMINATE",
        )

        termination = TextMentionTermination(text="TERMINATE")
        max_msg_termination = MaxMessageTermination(max_messages=6)
        combined_termination = max_msg_termination & termination
        team = RoundRobinGroupChat(
            participants=[
                # user_proxy_agent,
                planner_agent,
                language_agent,
                summary_agent,
            ],
            termination_condition=combined_termination,
        )
        team.component_version = 2
        team.component_label = "default_chat_team"
        team.component_description = "默认聊天团队"
        return team
