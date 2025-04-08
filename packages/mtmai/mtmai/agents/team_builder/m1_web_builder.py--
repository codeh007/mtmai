from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.teams import MagenticOneGroupChat
from autogen_core.models import ChatCompletionClient

# from autogen_magentic_one.agents.multimodal_web_surfer import MultimodalWebSurfer
# from autogen_magentic_one.agents.orchestrator import RoundRobinOrchestrator
# from autogen_magentic_one.agents.user_proxy import UserProxy
# from autogen_magentic_one.messages import RequestReplyMessage
# from autogen_magentic_one.utils import LogHandler


def percentage_change_tool(start: float, end: float) -> float:
    return ((end - start) / start) * 100


class M1WebTeamBuilder:
    """默认AI助理团"""

    @property
    def name(self):
        return "magentic_one_web_example"

    @property
    def description(self):
        return "magentic_one_web 演示"

    async def create_team(self, model_client: ChatCompletionClient = None):
        assistant = AssistantAgent(
            "Assistant",
            model_client=model_client,
        )
        team = MagenticOneGroupChat([assistant], model_client=model_client)
        return team
