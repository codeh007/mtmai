import logging
from typing import List
# from autogen_core import Component, DefaultTopicId, MessageContext, RoutedAgent, default_subscription, message_handler
from autogen_agentchat.agents._user_proxy_agent import UserProxyAgentConfig
from autogen_agentchat.agents import UserProxyAgent
from autogen_agentchat.base import ChatAgent, TerminationCondition
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.teams._group_chat._round_robin_group_chat import (
    RoundRobinGroupChatConfig,
)
# from mtmaisdk.clients.rest.models.ag_event_create import AgEventCreate
# from mtmaisdk.clients.rest.models.agent_run_input import AgentRunInput
# from mtmaisdk.clients.rest.models.chat_message import ChatMessage
# from mtmaisdk.clients.rest.models.chat_message_create import ChatMessageCreate
# from mtmaisdk.clients.rest_client import AsyncRestApi
# from pydantic import BaseModel
# from autogen_agentchat.messages import TextMessage
# from autogen_agentchat.base import TaskResult, Team

from autogen_core import (
    AgentId,
    DefaultSubscription,
    DefaultTopicId,
    MessageContext,
    RoutedAgent,
    message_handler,
)
logger = logging.getLogger(__name__)


class MtWebUserProxyAgent(UserProxyAgent):
    """扩展 UserProxyAgent"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


    def _to_config(self) -> UserProxyAgentConfig:
        # TODO: Add ability to serialie input_func
        return UserProxyAgentConfig(name=self.name, description=self.description, input_func=None)

class MtRoundRobinGroupChatConfig(RoundRobinGroupChatConfig):
    """扩展 RoundRobinGroupChatConfig"""

    # user_proxy_agent_name: str = "user_proxy_agent"
    pass


class MtRoundRobinGroupChat(
    RoundRobinGroupChat, Component[MtRoundRobinGroupChatConfig]
):
    """扩展 RoundRobinGroupChat"""

    component_provider_override = (
        "mtmai.agents._agents.RoundRobinGroupChat"
    )

    def __init__(
        self,
        participants: List[ChatAgent],
        termination_condition: TerminationCondition | None = None,
        max_turns: int | None = None,
    ):
        super().__init__(participants, termination_condition, max_turns)

