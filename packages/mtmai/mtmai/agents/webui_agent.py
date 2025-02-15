import logging
from typing import Any, Mapping

from autogen_core import (
    MessageContext,
    RoutedAgent,
    default_subscription,
    message_handler,
)
from team_builder import assisant_team_builder

from ..mtmaisdk.clients.rest.exceptions import ApiException
from ..mtmaisdk.clients.rest.models.ag_event_create import AgEventCreate
from ..mtmaisdk.clients.rest.models.ag_state_upsert import AgStateUpsert
from ..mtmaisdk.clients.rest.models.chat_message_upsert import ChatMessageUpsert
from ..mtmaisdk.clients.rest.models.task_result import TaskResult
from ..mtmaisdk.clients.rest.models.team import Team
from ..mtmaisdk.clients.rest.models.team_component import TeamComponent
from ..mtmaisdk.clients.rest.models.tenant_seed_req import TenantSeedReq
from ..mtmaisdk.hatchet import Hatchet
from ..team_builder.company_research import CompanyResearchTeamBuilder
from ..team_builder.travel_builder import TravelTeamBuilder
from ._types import ApiSaveTeamState, ApiSaveTeamTaskResult
from .model_client import MtmOpenAIChatCompletionClient

logger = logging.getLogger(__name__)


@default_subscription
class UIAgent(RoutedAgent):
    """
    UI Agent 是 UI 和 Worker 之间的桥梁, 负责处理 UI 发送的消息,
        1: 将状态通过SSE 推送到web 前端,
        2: 将消息和状态持久化到数据库
    """

    def __init__(self, wfapp: Hatchet) -> None:
        super().__init__("UI Agent")
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

    @message_handler
    async def handle_ag_event(
        self, message: AgEventCreate, ctx: MessageContext
    ) -> None:
        # tenant_id=get_tenant_id()
        logger.info("TODO: AgEventCreate")

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
        self, message: TenantSeedReq, mctx: MessageContext
    ) -> None:
        if not message.tenant_id or len(message.tenant_id) == 0:
            raise ValueError("tenantId required")
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
        # model_dict["model_info"] = model_dict.pop("model_info", None)
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
