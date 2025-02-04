import logging
import time
from pathlib import Path
from typing import AsyncGenerator, Callable, Optional, Union

from autogen_agentchat.base import TaskResult, Team
from autogen_agentchat.messages import AgentEvent, ChatMessage
from autogen_core import CancellationToken, Component, ComponentModel

from ...models.ag import TeamResult

logger = logging.getLogger(__name__)


class TeamRunner:
    """Team Runner"""

    async def _create_team(
        self,
        team_config: Union[str, Path, dict, ComponentModel],
        input_func: Optional[Callable] = None,
    ) -> Component:
        """Create team instance from config"""
        # Handle different input types
        if isinstance(team_config, (str, Path)):
            config = await self.load_from_file(team_config)
        elif isinstance(team_config, dict):
            config = team_config
        else:
            config = team_config.model_dump()

        # Use Component.load_component directly
        team = Team.load_component(config)

        for agent in team._participants:
            if hasattr(agent, "input_func"):
                agent.input_func = input_func

        # TBD - set input function
        return team
    async def run_stream(
        self,
        task: str,
        team_config: Union[str, Path, dict, ComponentModel],
        input_func: Optional[Callable] = None,
        cancellation_token: Optional[CancellationToken] = None,
    ) -> AsyncGenerator[Union[AgentEvent | ChatMessage, ChatMessage, TaskResult], None]:
        """Stream team execution results"""
        start_time = time.time()
        team = None

        try:
            team = await self._create_team(team_config, input_func)

            async for message in team.run_stream(
                task=task, cancellation_token=cancellation_token
            ):
                if cancellation_token and cancellation_token.is_cancelled():
                    break

                if isinstance(message, TaskResult):
                    yield TeamResult(
                        task_result=message, usage="", duration=time.time() - start_time
                    )
                else:
                    yield message

        finally:
            # Ensure cleanup happens
            if team and hasattr(team, "_participants"):
                for agent in team._participants:
                    if hasattr(agent, "close"):
                        await agent.close()
