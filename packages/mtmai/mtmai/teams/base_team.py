from abc import ABC
from typing import Any, List, Mapping, Sequence

from autogen_agentchat.base import TaskResult
from autogen_agentchat.messages import ChatMessage
from autogen_agentchat.state import TeamState
from autogen_agentchat.teams import BaseGroupChat
from autogen_core import CancellationToken, Component, ComponentModel
from pydantic import BaseModel


class BaseTeamConfig(BaseModel):
    participants: List[ComponentModel]
    termination_condition: ComponentModel | None = None
    max_turns: int | None = None


class MtBaseTeam(BaseGroupChat, ABC, Component[BaseTeamConfig]):
    component_type = "mtmai.teams.base_team.MtBaseTeam"

    def __init__(self):
        super().__init__()

    async def run(
        self,
        *,
        task: str | ChatMessage | Sequence[ChatMessage] | None = None,
        cancellation_token: CancellationToken | None = None,
    ) -> TaskResult:
        result: TaskResult | None = None
        async for message in self.run_stream(
            task=task,
            cancellation_token=cancellation_token,
        ):
            if isinstance(message, TaskResult):
                result = message
        if result is not None:
            return result
        raise AssertionError("The stream should have returned the final result.")

    async def reset(self) -> None: ...
    async def save_state(self) -> Mapping[str, Any]:
        """Save the state of the group chat team."""
        if not self._initialized:
            raise RuntimeError(
                "The group chat has not been initialized. It must be run before it can be saved."
            )

        if self._is_running:
            raise RuntimeError("The team cannot be saved while it is running.")
        self._is_running = True

        try:
            # Save the state of the runtime. This will save the state of the participants and the group chat manager.
            agent_states = await self._runtime.save_state()
            return TeamState(
                agent_states=agent_states, team_id=self._team_id
            ).model_dump()
        finally:
            # Indicate that the team is no longer running.
            self._is_running = False

    async def load_state(self, state: Mapping[str, Any]) -> None:
        """Load the state of the group chat team."""
        if not self._initialized:
            await self._init(self._runtime)

        if self._is_running:
            raise RuntimeError("The team cannot be loaded while it is running.")
        self._is_running = True

        try:
            # Load the state of the runtime. This will load the state of the participants and the group chat manager.
            team_state = TeamState.model_validate(state)
            self._team_id = team_state.team_id
            await self._runtime.load_state(team_state.agent_states)
        finally:
            # Indicate that the team is no longer running.
            self._is_running = False
