import asyncio
from typing import Any, AsyncGenerator, Callable, List, Mapping, Sequence

from autogen_agentchat.base import ChatAgent, TaskResult, TerminationCondition
from autogen_agentchat.messages import AgentEvent, ChatMessage
from autogen_agentchat.teams import BaseGroupChat
from autogen_agentchat.teams._group_chat._base_group_chat_manager import (
    BaseGroupChatManager,
)
from autogen_agentchat.teams._group_chat._round_robin_group_chat import (
    RoundRobinGroupChatConfig,
    RoundRobinGroupChatManager,
)
from autogen_agentchat.teams._group_chat._selector_group_chat import (
    SelectorGroupChatManager,
)
from autogen_core import (
    AgentRuntime,
    CancellationToken,
    Component,
    SingleThreadedAgentRuntime,
)
from mtmai.agents.intervention_handlers import NeedsUserInputHandler
from mtmai.clients.rest.models.component_model import ComponentModel
from mtmai.context.context_client import TenantClient
from mtmai.context.ctx import get_chat_session_id_ctx
from typing_extensions import Self


class InstagramTeamConfig(RoundRobinGroupChatConfig):
    manager_name: str = "RoundRobinGroupChatManager"


class InstagramTeam(BaseGroupChat, Component[InstagramTeamConfig]):
    component_provider_override = "mtmai.teams.instagram_team.InstagramTeam"
    component_config_schema = InstagramTeamConfig

    def __init__(
        self,
        participants: List[ComponentModel] = [],
        manager_name: str = "RoundRobinGroupChatManager",
        termination_condition: TerminationCondition | None = None,
        max_turns: int | None = None,
        runtime: AgentRuntime | None = None,
    ) -> None:
        self.tenant_client = TenantClient()
        self.manager_name = manager_name

        super().__init__(
            participants=participants,
            group_chat_manager_name=manager_name,
            group_chat_manager_class=RoundRobinGroupChatManager,
            termination_condition=termination_condition,
            max_turns=max_turns,
            runtime=runtime,
        )

    def _create_group_chat_manager_factory(
        self,
        name: str,
        group_topic_type: str,
        output_topic_type: str,
        participant_topic_types: List[str],
        participant_names: List[str],
        participant_descriptions: List[str],
        output_message_queue: asyncio.Queue[AgentEvent | ChatMessage],
        termination_condition: TerminationCondition | None,
        max_turns: int | None,
    ) -> Callable[[], BaseGroupChatManager]:
        def _factory() -> RoundRobinGroupChatManager:
            if self.manager_name == "RoundRobinGroupChatManager":
                return RoundRobinGroupChatManager(
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
            elif self.manager_name == "SelectorGroupChatManager":
                return SelectorGroupChatManager(
                    name,
                    group_topic_type,
                    output_topic_type,
                    participant_topic_types,
                    participant_names,
                    participant_descriptions,
                    output_message_queue,
                    termination_condition,
                    max_turns,
                    self._model_client,
                    self._selector_prompt,
                    self._allow_repeated_speaker,
                    self._selector_func,
                    self._max_selector_attempts,
                    self._candidate_func,
                )
            else:
                raise ValueError(f"Invalid manager name: {self.manager_name}")

        return _factory

    async def _init(self, runtime: AgentRuntime):
        self.session_id = get_chat_session_id_ctx()
        await super()._init(runtime)
        runtime.start()

    async def run_stream(
        self,
        *,
        task: str | ChatMessage | Sequence[ChatMessage] | None = None,
        cancellation_token: CancellationToken | None = None,
    ) -> AsyncGenerator[AgentEvent | ChatMessage | TaskResult, None]:
        if not self._initialized:
            await self._init(self._runtime)
        async for event in super().run_stream(
            task=task, cancellation_token=cancellation_token
        ):
            if isinstance(event, TaskResult):
                yield event
            else:
                await self.tenant_client.emit(event)
                yield event

        await self.tenant_client.ag.save_team_state(
            team=self,
            componentId=self._team_id,
            tenant_id=self.tenant_client.tenant_id,
            chat_id=self.session_id,
        )

    async def reset(self) -> None:
        # if not self._initialized:
        #     await self._init(self._runtime)

        # if self._is_running:
        #     raise RuntimeError("The group chat is currently running. It must be stopped before it can be reset.")
        # self._is_running = True

        # if self._embedded_runtime:
        #     # Start the runtime.
        #     assert isinstance(self._runtime, SingleThreadedAgentRuntime)
        #     self._runtime.start()

        # try:
        #     # Send a reset messages to all participants.
        #     for participant_topic_type in self._participant_topic_types:
        #         await self._runtime.send_message(
        #             GroupChatReset(),
        #             recipient=AgentId(type=participant_topic_type, key=self._team_id),
        #         )
        #     # Send a reset message to the group chat manager.
        #     await self._runtime.send_message(
        #         GroupChatReset(),
        #         recipient=AgentId(type=self._group_chat_manager_topic_type, key=self._team_id),
        #     )
        # finally:
        #     if self._embedded_runtime:
        #         # Stop the runtime.
        #         assert isinstance(self._runtime, SingleThreadedAgentRuntime)
        #         await self._runtime.stop_when_idle()

        #     # Reset the output message queue.
        #     while not self._output_message_queue.empty():
        #         self._output_message_queue.get_nowait()

        #     # Indicate that the team is no longer running.
        self._is_running = False

    async def save_state(self) -> Mapping[str, Any]:
        # state = RoundRobinManagerState(
        #     message_thread=list(self._message_thread),
        #     current_turn=self._current_turn,
        #     next_speaker_index=self._next_speaker_index,
        # )
        # return state.model_dump()
        state = await super().save_state()
        return state

    async def load_state(self, state: Mapping[str, Any]) -> None:
        await super().load_state(state)

    def _to_config(self) -> InstagramTeamConfig:
        participants = [
            participant.dump_component() for participant in self._participants
        ]
        termination_condition = (
            self._termination_condition.dump_component()
            if self._termination_condition
            else None
        )
        return InstagramTeamConfig(
            participants=participants,
            termination_condition=termination_condition,
            max_turns=self._max_turns,
        )

    @classmethod
    def _from_config(cls, config: InstagramTeamConfig) -> Self:
        session_id = get_chat_session_id_ctx()
        participants = []
        # if hasattr(config, "actual_instance"):
        #     config = config.actual_instance
        # if hasattr(config.participants, "actual_instance"):
        #     config.participants = config.participants.actual_instance
        # config.participants[0].oneof_schema_1_validator.
        for participant in config.participants:
            # if hasattr(participant, "actual_instance") and participant.actual_instance:
            #     participant = participant.actual_instance
            # participant_config = participant.model_dump()
            participants.append(ChatAgent.load_component(participant))
        termination_condition = (
            TerminationCondition.load_component(
                config.termination_condition.model_dump()
            )
            if config.termination_condition
            else None
        )

        needs_user_input_handler = NeedsUserInputHandler(session_id)
        runtime = SingleThreadedAgentRuntime(
            intervention_handlers=[needs_user_input_handler],
            ignore_unhandled_exceptions=False,
        )
        manager_name = config.manager_name
        return cls(
            participants=participants,
            manager_name=manager_name,
            termination_condition=termination_condition,
            max_turns=config.max_turns,
            runtime=runtime,
        )
        #     max_turns=config.max_turns,
        #     runtime=runtime,
        # )
