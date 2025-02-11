import logging
from typing import List

from autogen_agentchat.base import ChatAgent, TerminationCondition
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.teams._group_chat._round_robin_group_chat import (
    RoundRobinGroupChatConfig,
)
from autogen_core import Component

logger = logging.getLogger(__name__)


class MtRoundRobinGroupChatConfig(RoundRobinGroupChatConfig):
    """扩展 RoundRobinGroupChatConfig"""

    # user_proxy_agent_name: str = "user_proxy_agent"
    pass


class MtRoundRobinGroupChat(
    RoundRobinGroupChat, Component[MtRoundRobinGroupChatConfig]
):
    """扩展 RoundRobinGroupChat"""

    component_provider_override = (
        "mtmai.ag.base.RoundRobinGroupChat.MtRoundRobinGroupChat"
    )

    def __init__(
        self,
        participants: List[ChatAgent],
        termination_condition: TerminationCondition | None = None,
        max_turns: int | None = None,
    ):
        # 检查是否已经包含 user_proxy_agent
        # has_user_proxy = False
        # for participant in participants:
        #     if isinstance(participant, MtWebUserProxyAgent):
        #         has_user_proxy = True
        #         break

        # if not has_user_proxy:
        #     participants = [
        #         MtWebUserProxyAgent(
        #             name="user_proxy_agent",
        #         )
        #     ] + participants
        super().__init__(participants, termination_condition, max_turns)

    # async def run_stream(self, *args, **kwargs):
    #     return await super().run_stream(*args, **kwargs)

    # @classmethod
    # def _from_config(
    #     cls, config: MtRoundRobinGroupChatConfig
    # ) -> "MtRoundRobinGroupChat":
    #     return cls(
    #         name=config.name,
    #         participants=config.participants,
    #         termination_condition=config.termination_condition,
    #         max_turns=config.max_turns,
    #     )
