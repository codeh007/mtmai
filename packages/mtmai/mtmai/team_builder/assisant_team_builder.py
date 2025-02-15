import logging

from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.conditions import (MaxMessageTermination,
                                          TextMentionTermination)
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_core.models import ChatCompletionClient

from .__init__ import current_team_version

logger = logging.getLogger(__name__)


class AssistantTeamBuilder:
    """默认聊天团队"""

    @property
    def name(self):
        return "assistant_team"

    @property
    def description(self):
        return "默认聊天团队"

    async def create_team(self, default_model_client: ChatCompletionClient):
        planner_agent = AssistantAgent(
            name="planner_agent",
            model_client=default_model_client,
            description="足球赛事分析",
            system_message="你是足球赛事分析专家，可以分析足球赛事，并给出分析结果",
        )
        language_agent = AssistantAgent(
            name="投注建议专家",
            model_client=default_model_client,
            description="投注建议专家，可以给出投注建议",
            system_message="你是投注建议专家，可以给出投注建议",
        )

        summary_agent = AssistantAgent(
            name="足彩助理",
            model_client=default_model_client,
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
        team.component_version = current_team_version
        team.component_label = self.get_name()
        team.component_description = self.description
        return team
