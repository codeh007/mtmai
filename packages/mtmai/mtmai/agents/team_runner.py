import logging
import time
from pathlib import Path
from typing import Callable, Optional, Union

from autogen_agentchat.base import TaskResult, Team
from autogen_agentchat.messages import TextMessage
from autogen_core import CancellationToken, Component, ComponentModel
from mtmaisdk.clients.rest.models.ag_state_upsert import AgStateUpsert
from mtmaisdk.clients.rest.models.agent_run_input import AgentRunInput
from mtmaisdk.clients.rest_client import AsyncRestApi
from pydantic import BaseModel

from mtmai.models.ag import TeamResult
logger = logging.getLogger(__name__)


class TeamRunner:
    """Team Runner"""
    def __init__(self, gomtmapi: AsyncRestApi) -> None:
        self.gomtmapi=gomtmapi

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
        input: AgentRunInput,
        input_func: Optional[Callable] = None,
        cancellation_token: Optional[CancellationToken] = None,
    ):
        start_time = time.time()
        team_data = await self.gomtmapi.teams_api.team_get(
            tenant=input.tenant_id, team=input.team_id
        )
        if team_data is None:
            raise ValueError("team not found")

        team = await self._create_team(team_data.component)
        try:
            async for event in team.run_stream(
                task=input.task,
            ):
                if cancellation_token and cancellation_token.is_cancelled():
                    break
                # if isinstance(event, TextMessage):
                #     yield event.model_dump()
                # elif isinstance(event, BaseModel):
                #     yield event.model_dump()
                # elif isinstance(event, TaskResult):
                #     yield TeamResult(
                #         task_result=event, usage="", duration=time.time() - start_time
                #     )
                else:
                    yield event
            state_to_save = await team.save_state()
            # 保存状态
            saveed_response = (
                await self.gomtmapi.ag_state_api.ag_state_upsert(
                    tenant=input.tenant_id,
                    state=input.team_id,
                    ag_state_upsert=AgStateUpsert(
                        # id=team_id,
                        # version=state_to_save.get("version"),
                        state=state_to_save,
                        # type=state_to_save.get("type"),
                    ),
                )
            )
            logger.info(f"saveed_response: {saveed_response}")
        except Exception as e:
            logger.error(f"未知错误: {e}")
            raise e
        finally:
            # Ensure cleanup happens
            if team and hasattr(team, "_participants"):
                for agent in team._participants:
                    if hasattr(agent, "close"):
                        await agent.close()
