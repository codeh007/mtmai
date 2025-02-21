from autogen_core import (
    MessageContext,
    RoutedAgent,
    default_subscription,
    message_handler,
)
from loguru import logger
from mtmai.hatchet import Hatchet
from pydantic import BaseModel

from ...clients.rest.models.mt_component import MtComponent
from ...mtlibs.id import generate_uuid
from ..model_client import MtmOpenAIChatCompletionClient
from ..team_builder.article_gen_teambuilder import ArticleGenTeamBuilder
from ..team_builder.assisant_team_builder import AssistantTeamBuilder
from ..team_builder.m1_web_builder import M1WebTeamBuilder
from ..team_builder.swram_team_builder import SwramTeamBuilder
from ..team_builder.travel_builder import TravelTeamBuilder


class MsgResetTenant(BaseModel):
    tenant_id: str


class MsgGetTeamComponent(BaseModel):
    tenant_id: str
    component_id: str


@default_subscription
class TenantAgent(RoutedAgent):
    """
    租户管理
    """

    def __init__(self, description: str, wfapp: Hatchet = None) -> None:
        if wfapp is not None:
            self.wfapp = wfapp
            self.gomtmapi = self.wfapp.rest.aio
        else:
            raise ValueError("ui_agent is required")
        self.team_builders = [
            AssistantTeamBuilder(),
            SwramTeamBuilder(),
            ArticleGenTeamBuilder(),
            M1WebTeamBuilder(),
            TravelTeamBuilder(),
        ]
        super().__init__(description)

    @message_handler
    async def on_message(self, message: MsgResetTenant, ctx: MessageContext) -> None:
        logger.info(f"TenantAgent 收到消息: {message}")
        tenant_id: str | None = message.tenant_id

        if not tenant_id:
            raise ValueError("tenant_id is required")
        await self.reset_tenant(tenant_id)
        return

    async def reset_tenant(self, tenant_id: str):
        """重置租户信息"""
        logger.info(f"TenantAgent 重置租户信息: {tenant_id}")
        teams_list = await self.gomtmapi.coms_api.coms_list(
            tenant=tenant_id, label="default"
        )
        if teams_list.rows and len(teams_list.rows) > 0:
            logger.info(f"获取到默认聊天团队 {teams_list.rows[0].metadata.id}")
            return teams_list.rows[0]
        defaultModel = await self.gomtmapi.model_api.model_get(
            tenant=tenant_id, model="default"
        )
        model_dict = defaultModel.config.model_dump()
        model_dict.pop("n", None)
        model_client = MtmOpenAIChatCompletionClient(
            **model_dict,
        )
        for team_builder in self.team_builders:
            label = team_builder.name
            logger.info(f"create team for tenant {tenant_id}")
            team_comp = await team_builder.create_team(model_client)
            component_model = team_comp.dump_component()
            new_team = await self.gomtmapi.coms_api.coms_upsert(
                tenant=tenant_id,
                com=generate_uuid(),
                mt_component=MtComponent(
                    label=label,
                    description=component_model.description or "",
                    componentType="team",
                    component=component_model.model_dump(),
                ).model_dump(),
            )
