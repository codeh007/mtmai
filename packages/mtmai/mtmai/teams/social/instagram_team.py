import asyncio
from typing import Any, AsyncGenerator, Callable, List, Mapping, Sequence

from autogen_agentchat.base import ChatAgent, TaskResult, TerminationCondition
from autogen_agentchat.messages import AgentEvent, ChatMessage, MessageFactory
from autogen_agentchat.teams import BaseGroupChat
from autogen_agentchat.teams._group_chat._events import GroupChatTermination
from autogen_agentchat.teams._group_chat._magentic_one._prompts import (
    ORCHESTRATOR_FINAL_ANSWER_PROMPT,
)
from autogen_core import (
    AgentRuntime,
    CancellationToken,
    Component,
    ComponentModel,
    SingleThreadedAgentRuntime,
)
from autogen_core.models import ChatCompletionClient
from mtmai.agents.intervention_handlers import NeedsUserInputHandler
from mtmai.context.context_client import TenantClient
from mtmai.context.ctx import get_chat_session_id_ctx
from mtmai.model_client.utils import get_default_model_client
from mtmai.teams.social.instagram_manager import InstagramOrchestrator
from pydantic import BaseModel
from typing_extensions import Self


class InstagramTeamConfig(BaseModel):
    """The declarative configuration for a MagenticOneGroupChat."""

    participants: List[ComponentModel]
    model_client: ComponentModel
    termination_condition: ComponentModel | None = None
    max_turns: int | None = None
    max_stalls: int
    final_answer_prompt: str


class InstagramTeam(BaseGroupChat, Component[InstagramTeamConfig]):
    component_provider_override = "mtmai.teams.social.instagram_team.InstagramTeam"
    component_config_schema = InstagramTeamConfig

    def __init__(
        self,
        participants: List[ChatAgent],
        model_client: ChatCompletionClient,
        *,
        termination_condition: TerminationCondition | None = None,
        max_turns: int | None = 20,
        runtime: AgentRuntime | None = None,
        max_stalls: int = 3,
        final_answer_prompt: str = ORCHESTRATOR_FINAL_ANSWER_PROMPT,
        username: str | None = None,
        password: str | None = None,
    ) -> None:
        super().__init__(
            participants,
            group_chat_manager_name="InstagramOrchestrator",
            group_chat_manager_class=InstagramOrchestrator,
            termination_condition=termination_condition,
            max_turns=max_turns,
            runtime=runtime,
        )

        # Validate the participants.
        if len(participants) == 0:
            raise ValueError(
                "At least one participant is required for MagenticOneGroupChat."
            )
        self._model_client = model_client
        self._max_stalls = max_stalls
        self._final_answer_prompt = final_answer_prompt
        self._username = username
        self._password = password

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
        message_factory: MessageFactory,
    ) -> Callable[[], InstagramOrchestrator]:
        return lambda: InstagramOrchestrator(
            name,
            group_topic_type,
            output_topic_type,
            participant_topic_types,
            participant_names,
            participant_descriptions,
            max_turns,
            message_factory,
            self._model_client,
            self._max_stalls,
            self._final_answer_prompt,
            output_message_queue,
            termination_condition,
            username=self._username,
            password=self._password,
        )

    async def _init(self, runtime: AgentRuntime):
        self.session_id = get_chat_session_id_ctx()
        await super()._init(runtime)
        self._initialized = True
        self.tenant_client = TenantClient()
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

        state = await self.save_state()
        await self.tenant_client.ag.save_team_state(
            componentId=self._team_id,
            tenant_id=self.tenant_client.tenant_id,
            chat_id=self.session_id,
            state=state,
        )

    async def reset(self) -> None:
        self._is_running = False

    async def save_state(self) -> Mapping[str, Any]:
        state = await super().save_state()
        return {
            "some_state": "some_state",
            **state,
        }

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
            model_client=self._model_client.dump_component(),
            termination_condition=termination_condition,
            max_turns=self._max_turns,
            max_stalls=self._max_stalls,
            final_answer_prompt=self._final_answer_prompt,
        )

    @classmethod
    def _from_config(cls, config: InstagramTeamConfig) -> Self:
        session_id = get_chat_session_id_ctx()
        participants = []
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
        if config.model_client:
            model_client = ChatCompletionClient.load_component(config.model_client)

        else:
            model_client = get_default_model_client()

        return cls(
            participants=participants,
            termination_condition=termination_condition,
            runtime=runtime,
            model_client=model_client,
            max_turns=config.max_turns or 20,
            max_stalls=config.max_stalls or 3,
            final_answer_prompt=config.final_answer_prompt
            or ORCHESTRATOR_FINAL_ANSWER_PROMPT,
            username=config.username,
            password=config.password,
        )

    async def pause(self) -> None:
        """Pause the team and all its participants. This is useful for
        pausing the :meth:`autogen_agentchat.base.TaskRunner.run` or
        :meth:`autogen_agentchat.base.TaskRunner.run_stream` methods from
        concurrently, while keeping them alive."""
        ...

    async def resume(self) -> None:
        """Resume the team and all its participants from a pause after
        :meth:`pause` was called."""
        ...
