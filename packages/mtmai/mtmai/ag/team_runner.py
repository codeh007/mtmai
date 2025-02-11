import logging
import time
from pathlib import Path
from typing import AsyncGenerator, Callable, Optional, Union

from autogen_agentchat.base import TaskResult, Team
from autogen_agentchat.messages import AgentEvent, ChatMessage, TextMessage
from autogen_core import CancellationToken, Component, ComponentModel
from mtmaisdk.clients.rest.models.ag_state import AgState
from mtmaisdk.context.context import Context
from pydantic import BaseModel

from mtmai.ag.team_builder import TeamBuilder
from mtmai.agents.ctx import get_mtmai_context
from mtmai.models.ag import TeamResult

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

    async def run_stream_v2(
        self,
        hatctx: Context,
        task: str,
        team_id: str,
        # team_config: Union[str, Path, dict, ComponentModel],
        input_func: Optional[Callable] = None,
        cancellation_token: Optional[CancellationToken] = None,
    ):
        ctx = get_mtmai_context()

        tenant_id = ctx.getTenantId()
        team_data = await ctx.hatchet_ctx.rest_client.aio.teams_api.team_get(
            tenant=tenant_id, team=team_id
        )
        if team_data is None:
            raise ValueError("team not found")

        team_builder = TeamBuilder()
        team = await team_builder.create_team(team_data.component)
        start_time = time.time()
        try:
            async for event in team.run_stream(
                task=task,
                # team_config=agent.dump_component()
            ):
                if cancellation_token and cancellation_token.is_cancelled():
                    break
                if isinstance(event, TextMessage):
                    yield event.model_dump()
                elif isinstance(event, BaseModel):
                    yield event.model_dump()
                elif isinstance(event, TaskResult):
                    yield TeamResult(
                        task_result=event, usage="", duration=time.time() - start_time
                    )
                else:
                    yield event.model_dump()
            state_to_save = await team.save_state()
            logger.info(f"state2: {state_to_save}")

            # 保存状态
            saveed_response = (
                await ctx.hatchet_ctx.rest_client.aio.ag_state_api.ag_state_upsert(
                    tenant=tenant_id,
                    state=team_id,
                    ag_state=AgState(
                        version=state_to_save.get("version", "1.0.0"),
                        teamId=state_to_save.get("team_id"),
                        state=state_to_save,
                        type=state_to_save.get("type", "team"),
                    ),
                )
            )
            logger.info(f"saveed_response: {saveed_response}")
        finally:
            # Ensure cleanup happens
            if team and hasattr(team, "_participants"):
                for agent in team._participants:
                    if hasattr(agent, "close"):
                        await agent.close()
