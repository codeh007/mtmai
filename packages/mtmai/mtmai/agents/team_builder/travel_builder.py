from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.conditions import MaxMessageTermination, TextMentionTermination
from autogen_core.models import ChatCompletionClient

from mtmai.agents._agents import MtRoundRobinGroupChat

from .__init__ import current_team_version


class TravelTeamBuilder:
    """Manages team operations including loading configs and running teams"""

    @property
    def name(self):
        return "travel_agent"

    @property
    def description(self):
        return "行程规划团队"

    async def create_team(self, default_model_client: ChatCompletionClient = None):
        planner_agent = AssistantAgent(
            name="planner_agent",
            model_client=default_model_client,
            description="A helpful assistant that can plan trips.",
            system_message="You are a helpful assistant that can suggest a travel plan for a user based on their request.",
        )

        local_agent = AssistantAgent(
            name="local_agent",
            model_client=default_model_client,
            description="A local assistant that can suggest local activities or places to visit.",
            system_message="You are a helpful assistant that can suggest authentic and interesting local activities or places to visit for a user and can utilize any context information provided.",
        )

        language_agent = AssistantAgent(
            name="language_agent",
            model_client=default_model_client,
            description="A helpful assistant that can provide language tips for a given destination.",
            system_message="You are a helpful assistant that can review travel plans, providing feedback on important/critical tips about how best to address language or communication challenges for the given destination. If the plan already includes language tips, you can mention that the plan is satisfactory, with rationale.",
        )

        travel_summary_agent = AssistantAgent(
            name="travel_summary_agent",
            model_client=default_model_client,
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
        team.component_version = current_team_version
        team.component_label = self.name
        team.component_description = self.description

        return team
