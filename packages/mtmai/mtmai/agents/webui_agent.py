import logging
from pathlib import Path
from typing import Any, Callable, Mapping, Optional, Union

from autogen_core import (
    Component,
    ComponentModel,
    MessageContext,
    RoutedAgent,
    default_subscription,
    message_handler,
)

from mtmai.clients.rest.exceptions import ApiException
from mtmai.clients.rest.models.ag_state_upsert import AgStateUpsert
from mtmai.clients.rest.models.chat_message_upsert import ChatMessageUpsert
from mtmai.clients.rest.models.task_result import TaskResult
from mtmai.clients.rest.models.team import Team
from mtmai.clients.rest.models.team_component import TeamComponent
from mtmai.hatchet import Hatchet
from mtmai.team_builder import assisant_team_builder
from mtmai.team_builder.company_research import CompanyResearchTeamBuilder
from mtmai.team_builder.travel_builder import TravelTeamBuilder

from ._types import ApiSaveTeamState, ApiSaveTeamTaskResult, MsgGetTeam
from .model_client import MtmOpenAIChatCompletionClient

logger = logging.getLogger(__name__)


@default_subscription
class UIAgent(RoutedAgent):
    """
    UI Agent 是 UI 和 Worker 之间的桥梁, 负责处理 UI 发送的消息,
        1: 将状态通过SSE 推送到web 前端,
        2: 将消息和状态持久化到数据库
    """

    def __init__(self, description: str, wfapp: Hatchet = None) -> None:
        super().__init__(description)
        if wfapp is not None:
            self.wfapp = wfapp
            self.gomtmapi = self.wfapp.rest.aio

    async def load_state(self, state: Mapping[str, Any]) -> None:
        """Load the state of the group chat team."""
        self.last_message = state["last_message"]

    @message_handler
    async def handle_message_create(
        self, message: ChatMessageUpsert, ctx: MessageContext
    ) -> None:
        # logger.info(f"UI Agent 收到消息: {message}")
        try:
            await self.gomtmapi.chat_api.chat_message_upsert(
                tenant=message.tenant_id,
                chat_message_upsert=ChatMessageUpsert(
                    tenantId=message.tenant_id,
                    teamId=message.team_id,
                    content=message.content,
                    role=message.role,
                    threadId=message.thread_id,
                ).model_dump(),
            )
        except ApiException as e:
            logger.error(f"UI Agent 保存消息失败: {e}")
            raise e
        except Exception as e:
            logger.error(f"UI Agent 保存消息失败(unknown error): {e}")
            raise e

    # @message_handler
    # async def handle_ag_event(
    #     self, message: AgEventCreate, ctx: MessageContext
    # ) -> None:
    #     # tenant_id=get_tenant_id()
    #     logger.info("TODO: AgEventCreate")

    @message_handler
    async def handle_task_result(
        self, message: TaskResult, ctx: MessageContext
    ) -> None:
        logger.info("TODO: TaskResult")

    @message_handler
    async def handle_api_save_team_state(
        self, message: ApiSaveTeamState, ctx: MessageContext
    ) -> None:
        """保存团队状态"""
        logger.info("保存团队状态")
        try:
            await self.gomtmapi.ag_state_api.ag_state_upsert(
                tenant=message.tenant_id,
                ag_state_upsert=AgStateUpsert(
                    componentId=message.componentId,
                    runId=message.runId,
                    state=message.state,
                ).model_dump(),
            )
        except Exception as e:
            logger.error(f"WorkerMainAgent 保存状态出错: {e}")

    @message_handler
    async def handle_api_save_team_task_result(
        self, message: ApiSaveTeamTaskResult, ctx: MessageContext
    ) -> None:
        """保存团队最终结果"""
        logger.info("TODO:UI Agent 保存任务结果")

    @message_handler
    async def handle_tenant_message(
        self, message: MsgGetTeam, mctx: MessageContext
    ) -> Team:
        # if not message.tenant_id or len(message.tenant_id) == 0:
        #     # raise ValueError("tenantId required")
        #     raise CantHandleException("tenantId required")
        tenant_id = message.tenant_id

        team_builters = [
            TravelTeamBuilder(),
            CompanyResearchTeamBuilder(),
            assisant_team_builder.AssistantTeamBuilder(),
        ]
        defaultModel = await self.gomtmapi.model_api.model_get(
            tenant=tenant_id, model="default"
        )
        model_dict = defaultModel.config.model_dump()
        model_dict.pop("n", None)
        model_client = MtmOpenAIChatCompletionClient(
            **model_dict,
        )
        for team_builder in team_builters:
            team = await team_builder.create_team(model_client)
            team_comp = team.dump_component()
            comp = TeamComponent(**team_comp.model_dump())
            team2 = Team(
                label=team_comp.label,
                description=team_comp.description or "",
                component=comp.model_dump(),
            )
            logger.info(
                f"create team for tenant: {message.tenant_id}, team: {team._team_id}"
            )
            await self.gomtmapi.team_api.team_upsert(
                tenant=message.tenant_id,
                team=team._team_id,
                team2=team2.model_dump(),
            )
        teams = await self.gomtmapi.teams_api.team_list(tenant=tenant_id)
        detault_team_item = next(
            (
                item
                for item in teams.rows
                if item.label == assisant_team_builder.AssistantTeamBuilder().name
            ),
            None,
        )

        return await self.gomtmapi.teams_api.team_get(
            tenant=tenant_id,
            team=detault_team_item.metadata.id,
        )

    async def _create_team_component(
        self,
        team_config: Union[str, Path, dict, ComponentModel],
        input_func: Optional[Callable] = None,
    ) -> Component:
        """Create team instance from config"""
        if isinstance(team_config, (str, Path)):
            config = await self.load_from_file(team_config)
        elif isinstance(team_config, dict):
            config = team_config
        else:
            config = team_config.model_dump()

        team = Team.load_component(config)

        for agent in team._participants:
            if hasattr(agent, "input_func"):
                agent.input_func = input_func

        return team
