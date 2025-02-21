from datetime import time
from typing import Any

from autogen_agentchat.base import Team
from autogen_core import (
    AgentId,
    MessageContext,
    RoutedAgent,
    default_subscription,
    message_handler,
)
from loguru import logger
from mtmai.hatchet import Hatchet
from pydantic import BaseModel

from ...mtlibs.id import generate_uuid
from ..team_builder.assisant_team_builder import AssistantTeamBuilder
from ..team_builder.swram_team_builder import SwramTeamBuilder


class MsgResetTenant(BaseModel):
    tenant_id: str


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
        ]
        super().__init__(description)

    @message_handler
    async def on_new_message(
        self, message: MsgResetTenant, ctx: MessageContext
    ) -> None:
        start_time = time.time()
        logger.info(f"TenantAgent 收到消息: {message}")
        tenant_id: str | None = message.tenant_id

        if not tenant_id:
            raise ValueError("tenant_id is required")
        # set_tenant_id(tenant_id)
        run_id = message.run_id
        if not run_id:
            raise ValueError("run_id is required")

        user_input = message.content
        if user_input.startswith("/tenant/seed"):
            logger.info(f"通知 TanantAgent 初始化(或重置)租户信息: {message}")
            # await self.runtime.publish_message(
            #     TenantSeedReq(tenantId=tenant_id),
            #     topic_id=DefaultTopicId(),
            # )
            return

        # ag_helper = AgHelper(self.gomtmapi)
        # if not message.team_id:
        #     assistant_team_builder = AssistantTeamBuilder()
        #     team = await ag_helper.get_or_create_default_team(
        #         tenant_id=message.tenant_id,
        #         label=assistant_team_builder.name,
        #     )
        #     message.team_id = team.metadata.id

        thread_id = message.session_id
        if not thread_id:
            thread_id = generate_uuid()

        team = Team.load_component(team_component_data.component.model_dump())
        team_id = message.team_id
        if not team_id:
            team_id = generate_uuid()

    async def send_ui_msg(self, message: Any):
        """发送UI消息

        Args:
            *messages: 可变参数,支持发送多条消息
        """
        target_agent_id = AgentId(type="ui_agent", key="default")
        return await self.send_message(
            message=message,
            recipient=target_agent_id,
        )

        # 学习:
        # 如果消息没法本智能体处理,应抛出异常: CantHandleException
