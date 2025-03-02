from abc import ABC
from typing import AsyncGenerator, List, Sequence

from autogen_agentchat.base import TaskResult, Team, TerminationCondition
from autogen_agentchat.messages import AgentEvent, ChatMessage
from autogen_core import CancellationToken, Component, ComponentModel
from pydantic import BaseModel

from ..context.context_client import TenantClient

# class MtAssisantTeamManager(BaseGroupChatManager):
#     """A group chat manager that selects the next speaker in a round-robin fashion."""

#     def __init__(
#         self,
#         group_topic_type: str,
#         output_topic_type: str,
#         participant_topic_types: List[str],
#         participant_descriptions: List[str],
#         termination_condition: TerminationCondition | None,
#         max_turns: int | None = None,
#     ) -> None:
#         super().__init__(
#             group_topic_type,
#             output_topic_type,
#             participant_topic_types,
#             participant_descriptions,
#             termination_condition,
#             max_turns,
#         )
#         self._next_speaker_index = 0

#     async def validate_group_state(self, messages: List[ChatMessage] | None) -> None:
#         pass

#     async def reset(self) -> None:
#         self._current_turn = 0
#         self._message_thread.clear()
#         if self._termination_condition is not None:
#             await self._termination_condition.reset()
#         self._next_speaker_index = 0

#     async def save_state(self) -> Mapping[str, Any]:
#         state = RoundRobinManagerState(
#             message_thread=list(self._message_thread),
#             current_turn=self._current_turn,
#             next_speaker_index=self._next_speaker_index,
#         )
#         return state.model_dump()

#     async def load_state(self, state: Mapping[str, Any]) -> None:
#         round_robin_state = RoundRobinManagerState.model_validate(state)
#         self._message_thread = list(round_robin_state.message_thread)
#         self._current_turn = round_robin_state.current_turn
#         self._next_speaker_index = round_robin_state.next_speaker_index

#     async def select_speaker(self, thread: List[AgentEvent | ChatMessage]) -> str:
#         """Select a speaker from the participants in a round-robin fashion."""
#         current_speaker_index = self._next_speaker_index
#         self._next_speaker_index = (current_speaker_index + 1) % len(
#             self._participant_topic_types
#         )
#         current_speaker = self._participant_topic_types[current_speaker_index]
#         return current_speaker


class MtAssisantTeamConfig(BaseModel):
    """The declarative configuration RoundRobinGroupChat."""

    participants: List[ComponentModel]
    termination_condition: ComponentModel | None = None
    max_turns: int | None = None


class MtAssisantTeam(Team, ABC, Component[MtAssisantTeamConfig]):
    # component_config_schema = MtAssisantTeamConfig
    component_type = "mtmai.teams.MtAssisantTeam"

    def __init__(
        self,
        # participants: List[ChatAgent],
        termination_condition: TerminationCondition | None = None,
        max_turns: int | None = None,
    ):
        super().__init__(
            # participants,
            # group_chat_manager_class=MtAssisantTeamManager,
            # termination_condition=termination_condition,
            # max_turns=max_turns,
        )

    async def run_stream(
        self,
        *,
        task: str | ChatMessage | Sequence[ChatMessage] | None = None,
        cancellation_token: CancellationToken | None = None,
    ) -> AsyncGenerator[AgentEvent | ChatMessage | TaskResult, None]:
        tenant_client = TenantClient()
        pass
