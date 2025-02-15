from autogen_agentchat.agents import AssistantAgent, UserProxyAgent
from autogen_agentchat.conditions import TextMentionTermination
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_core.models import ChatCompletionClient

from .__init__ import current_team_version


class SwramTeamBuilder:
    @property
    def name(self):
        return "swram_demo_team"

    @property
    def description(self):
        return "swram demo team"

    async def create_team(self, default_model_client: ChatCompletionClient = None):
        assistant = AssistantAgent("assistant", model_client=default_model_client)
        user_proxy = UserProxyAgent(
            "user_proxy", input_func=input
        )  # Use input() to get user input from console.

        # Create the termination condition which will end the conversation when the user says "APPROVE".
        termination = TextMentionTermination("APPROVE")

        # Create the team.
        team = RoundRobinGroupChat(
            [assistant, user_proxy], termination_condition=termination
        )

        # Run the conversation and stream to the console.
        # stream = team.run_stream(task="Write a 4-line poem about the ocean.")
        team.component_version = current_team_version
        team.component_label = self.name
        team.component_description = self.description
        return team
        return team
