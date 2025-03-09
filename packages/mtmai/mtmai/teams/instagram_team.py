import asyncio
from typing import Any, AsyncGenerator, Callable, List, Mapping

from autogen_agentchat.base import ChatAgent, TaskResult, TerminationCondition
from autogen_agentchat.messages import AgentEvent, ChatMessage, HandoffMessage
from autogen_agentchat.state import SwarmManagerState
from autogen_agentchat.teams._group_chat._base_group_chat_manager import (
    BaseGroupChatManager,
)
from autogen_agentchat.teams._group_chat._events import GroupChatTermination
from autogen_core import AgentRuntime, CancellationToken, Component, ComponentModel
from loguru import logger
from mtmai.agents._agents import MtAssistantAgent
from mtmai.clients.rest.models.chat_session_start_event import ChatSessionStartEvent
from mtmai.clients.rest.models.instagram_task import InstagramTask
from mtmai.clients.rest.models.platform_account_data import PlatformAccountData
from mtmai.context.context_client import TenantClient
from mtmai.context.ctx import get_chat_session_id_ctx, get_team_id_ctx
from mtmai.mtlibs.id import generate_uuid
from mtmai.teams.base_team import MtBaseTeam
from pydantic import BaseModel


class InstagramGroupChatManager(BaseGroupChatManager):
    """A group chat manager that selects the next speaker based on handoff message only."""

    def __init__(
        self,
        name: str,
        group_topic_type: str,
        output_topic_type: str,
        participant_topic_types: List[str],
        participant_names: List[str],
        participant_descriptions: List[str],
        output_message_queue: asyncio.Queue[
            AgentEvent | ChatMessage | GroupChatTermination
        ],
        termination_condition: TerminationCondition | None,
        max_turns: int | None,
    ) -> None:
        super().__init__(
            name,
            group_topic_type,
            output_topic_type,
            participant_topic_types,
            participant_names,
            participant_descriptions,
            output_message_queue,
            termination_condition,
            max_turns,
        )
        self._current_speaker = self._participant_names[0]

    async def validate_group_state(self, messages: List[ChatMessage] | None) -> None:
        """Validate the start messages for the group chat."""
        # Check if any of the start messages is a handoff message.
        if messages:
            for message in messages:
                if isinstance(message, HandoffMessage):
                    if message.target not in self._participant_names:
                        raise ValueError(
                            f"The target {message.target} is not one of the participants {self._participant_names}. "
                            "If you are resuming Swarm with a new HandoffMessage make sure to set the target to a valid participant as the target."
                        )
                    return

        # Check if there is a handoff message in the thread that is not targeting a valid participant.
        for existing_message in reversed(self._message_thread):
            if isinstance(existing_message, HandoffMessage):
                if existing_message.target not in self._participant_names:
                    raise ValueError(
                        f"The existing handoff target {existing_message.target} is not one of the participants {self._participant_names}. "
                        "If you are resuming Swarm with a new task make sure to include in your task "
                        "a HandoffMessage with a valid participant as the target. For example, if you are "
                        "resuming from a HandoffTermination, make sure the new task is a HandoffMessage "
                        "with a valid participant as the target."
                    )
                # The latest handoff message should always target a valid participant.
                # Do not look past the latest handoff message.
                return

    async def reset(self) -> None:
        self._current_turn = 0
        self._message_thread.clear()
        if self._termination_condition is not None:
            await self._termination_condition.reset()
        self._current_speaker = self._participant_names[0]

    async def select_speaker(self, thread: List[AgentEvent | ChatMessage]) -> str:
        """Select a speaker from the participants based on handoff message.
        Looks for the last handoff message in the thread to determine the next speaker."""
        if len(thread) == 0:
            return self._current_speaker
        for message in reversed(thread):
            if isinstance(message, HandoffMessage):
                self._current_speaker = message.target
                # The latest handoff message should always target a valid participant.
                assert self._current_speaker in self._participant_names
                return self._current_speaker
        return self._current_speaker

    async def save_state(self) -> Mapping[str, Any]:
        state = SwarmManagerState(
            message_thread=list(self._message_thread),
            current_turn=self._current_turn,
            current_speaker=self._current_speaker,
        )
        return state.model_dump()

    async def load_state(self, state: Mapping[str, Any]) -> None:
        swarm_state = SwarmManagerState.model_validate(state)
        self._message_thread = list(swarm_state.message_thread)
        self._current_turn = swarm_state.current_turn
        self._current_speaker = swarm_state.current_speaker


class InstagramTeamConfig(BaseModel):
    participants: List[ComponentModel]
    termination_condition: ComponentModel | None = None
    max_turns: int | None = None
    some_value: str = "some_value"
    result_id: str = None


class InstagramTeam(MtBaseTeam, Component[InstagramTeamConfig]):
    component_type = "mtmai.teams.instagram_team.InstagramTeam"

    def __init__(
        self,
        participants: List[ChatAgent] = [],
        termination_condition: TerminationCondition | None = None,
        max_turns: int | None = None,
        runtime: AgentRuntime | None = None,
    ) -> None:
        # 初始化参与者
        if not participants:
            participants = [
                MtAssistantAgent(
                    "InstagramAgent",
                    description="An agent for performing Instagram tasks.",
                )
            ]

        super().__init__(
            participants,
            group_chat_manager_name="InstagramGroupChatManager",
            group_chat_manager_class=InstagramGroupChatManager,
            termination_condition=termination_condition,
            max_turns=max_turns,
            runtime=runtime,
        )
        # The first participant must be able to produce handoff messages.
        first_participant = self._participants[0]
        if HandoffMessage not in first_participant.produced_message_types:
            raise ValueError(
                "The first participant must be able to produce a handoff messages."
            )

    def _create_group_chat_manager_factory(
        self,
        name: str,
        group_topic_type: str,
        output_topic_type: str,
        participant_topic_types: List[str],
        participant_names: List[str],
        participant_descriptions: List[str],
        output_message_queue: asyncio.Queue[
            AgentEvent | ChatMessage | GroupChatTermination
        ],
        termination_condition: TerminationCondition | None,
        max_turns: int | None,
    ) -> Callable[[], InstagramGroupChatManager]:
        def _factory() -> InstagramGroupChatManager:
            return InstagramGroupChatManager(
                name,
                group_topic_type,
                output_topic_type,
                participant_topic_types,
                participant_names,
                participant_descriptions,
                output_message_queue,
                termination_condition,
                max_turns,
            )

        return _factory

    async def run_stream(
        self,
        *,
        task: InstagramTask,
        cancellation_token: CancellationToken | None = None,
    ) -> AsyncGenerator[AgentEvent | ChatMessage | TaskResult, None]:
        tenant_client = TenantClient()
        tid = tenant_client.tenant_id
        # if task.startswith("/tenant/seed"):
        #     logger.info("通知 TanantAgent 初始化(或重置)租户信息")
        #     result = await self._runtime.send_message(
        #         MsgResetTenant(tenant_id=tid),
        #         self.tenant_agent_id,
        #     )
        #     return

        logger.info(f"Platform account agent received task: {task}")
        tenant_client = TenantClient()
        tid = tenant_client.tenant_id
        platform_account = await tenant_client.ag.resource_api.resource_get(
            tenant=tid,
            resource=task.resource_id,
        )
        platform_account_data = PlatformAccountData.model_validate(
            platform_account.content
        )
        logger.info(f"platform_account_data: {platform_account_data}")

        team_id = get_team_id_ctx() or generate_uuid()
        chat_id = get_chat_session_id_ctx() or generate_uuid()
        team = await tenant_client.ag.get_team()
        ag_state = await tenant_client.ag.load_team_state(
            tenant_id=tenant_client.tenant_id,
            chat_id=chat_id,
        )
        if ag_state:
            await team.load_state(ag_state.state)

        logger.info(f"运行: task: {task}, chat_id:{chat_id}")

        await tenant_client.emit(
            ChatSessionStartEvent(
                threadId=chat_id,
            )
        )

        try:
            async for event in team.run_stream(
                task=task,
                cancellation_token=cancellation_token,
            ):
                if cancellation_token and cancellation_token.is_cancelled():
                    break
                yield event
                await tenant_client.event.emit(event)

        finally:
            await tenant_client.ag.save_team_state(
                team=team,
                team_id=team_id,
                tenant_id=tenant_client.tenant_id,
                chat_id=chat_id,
            )
