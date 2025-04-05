import asyncio
import logging
from typing import Callable, List

from autogen_agentchat import EVENT_LOGGER_NAME, TRACE_LOGGER_NAME
from autogen_agentchat.base import ChatAgent, TerminationCondition
from autogen_agentchat.teams._group_chat._base_group_chat import BaseGroupChat
from autogen_agentchat.teams._group_chat._events import (
    AgentEvent,
    ChatMessage,
    GroupChatTermination,
)
from autogen_agentchat.teams._group_chat._magentic_one._magentic_one_orchestrator import (
    MagenticOneOrchestrator,
)
from autogen_agentchat.teams._group_chat._magentic_one._prompts import (
    ORCHESTRATOR_FINAL_ANSWER_PROMPT,
)
from autogen_core import AgentRuntime, Component, ComponentModel
from autogen_core.models import ChatCompletionClient
from pydantic import BaseModel
from typing_extensions import Self

trace_logger = logging.getLogger(TRACE_LOGGER_NAME)
event_logger = logging.getLogger(EVENT_LOGGER_NAME)


class MagenticOneGroupChatConfig(BaseModel):
    """The declarative configuration for a MagenticOneGroupChat."""

    participants: List[ComponentModel]
    model_client: ComponentModel
    termination_condition: ComponentModel | None = None
    max_turns: int | None = None
    max_stalls: int
    final_answer_prompt: str


class MagenticOneGroupChat(BaseGroupChat, Component[MagenticOneGroupChatConfig]):
    component_config_schema = MagenticOneGroupChatConfig
    component_provider_override = "mtmai.teams.m1team.MagenticOneGroupChat"

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
    ):
        super().__init__(
            participants,
            group_chat_manager_name="MagenticOneOrchestrator",
            group_chat_manager_class=MagenticOneOrchestrator,
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
    ) -> Callable[[], MagenticOneOrchestrator]:
        return lambda: MagenticOneOrchestrator(
            name,
            group_topic_type,
            output_topic_type,
            participant_topic_types,
            participant_names,
            participant_descriptions,
            max_turns,
            self._model_client,
            self._max_stalls,
            self._final_answer_prompt,
            output_message_queue,
            termination_condition,
        )

    def _to_config(self) -> MagenticOneGroupChatConfig:
        participants = [
            participant.dump_component() for participant in self._participants
        ]
        termination_condition = (
            self._termination_condition.dump_component()
            if self._termination_condition
            else None
        )
        return MagenticOneGroupChatConfig(
            participants=participants,
            model_client=self._model_client.dump_component(),
            termination_condition=termination_condition,
            max_turns=self._max_turns,
            max_stalls=self._max_stalls,
            final_answer_prompt=self._final_answer_prompt,
        )

    @classmethod
    def _from_config(cls, config: MagenticOneGroupChatConfig) -> Self:
        participants = [
            ChatAgent.load_component(participant) for participant in config.participants
        ]
        model_client = ChatCompletionClient.load_component(config.model_client)
        termination_condition = (
            TerminationCondition.load_component(config.termination_condition)
            if config.termination_condition
            else None
        )
        return cls(
            participants,
            model_client,
            termination_condition=termination_condition,
            max_turns=config.max_turns,
            max_stalls=config.max_stalls,
            final_answer_prompt=config.final_answer_prompt,
        )
