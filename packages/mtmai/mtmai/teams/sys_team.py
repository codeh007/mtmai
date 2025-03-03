from typing import AsyncGenerator, List, Sequence

from autogen_agentchat.base import TaskResult
from autogen_agentchat.messages import AgentEvent, ChatMessage
from autogen_core import CancellationToken, Component, ComponentModel
from loguru import logger
from mtmai.agents.team_builder.assisant_team_builder import AssistantTeamBuilder
from mtmai.agents.tenant_agent.tenant_agent import MsgResetTenant
from mtmai.context.context_client import TenantClient
from mtmai.context.ctx import get_chat_session_id_ctx, get_team_id_ctx
from mtmai.mtlibs.id import generate_uuid
from mtmai.mtmpb.events_pb2 import ChatSessionStartEvent
from mtmai.teams.base_team import MtBaseTeam
from pydantic import BaseModel


class SysTeamConfig(BaseModel):
    participants: List[ComponentModel]
    termination_condition: ComponentModel | None = None
    max_turns: int | None = None


class SysTeam(MtBaseTeam, Component[SysTeamConfig]):
    component_type = "mtmai.teams.sys_team.SysTeam"

    def __init__(self):
        super().__init__()

    async def run_stream(
        self,
        *,
        task: str | ChatMessage | Sequence[ChatMessage] | None = None,
        cancellation_token: CancellationToken | None = None,
    ) -> AsyncGenerator[AgentEvent | ChatMessage | TaskResult, None]:
        tenant_client = TenantClient()
        tid = tenant_client.tenant_id
        if task.startswith("/tenant/seed"):
            logger.info("通知 TanantAgent 初始化(或重置)租户信息")
            result = await self._runtime.send_message(
                MsgResetTenant(tenant_id=tid),
                self.tenant_agent_id,
            )
            return

        team_id = get_team_id_ctx()
        if not team_id:
            tenant_teams = await tenant_client.ag.list_team_component(tid)
            logger.info(f"get team component: {tenant_teams}")
            team_id = tenant_teams[0].metadata.id

        # team = await tenant_client.ag.get_team(tenant_client.tenant_id, team_id)
        model_client = await tenant_client.ag.get_default_model_client(tid)
        team = await AssistantTeamBuilder().create_team(model_client)

        if not team_id:
            team_id = generate_uuid()

        chat_id = get_chat_session_id_ctx()
        if not chat_id:
            chat_id = generate_uuid()

        else:
            # 加载团队状态
            # await self.load_state(thread_id)
            ...
        logger.info(f"chat session: {chat_id}")
        ag_state = await tenant_client.ag.load_team_state(
            tenant_id=tenant_client.tenant_id,
            chat_id=chat_id,
        )
        if ag_state:
            team.load_state(ag_state)
            logger.info("成功加载团队状态", component_type=team.component_type)

        await tenant_client.emit(
            ChatSessionStartEvent(
                threadId=chat_id,
            )
        )

        try:
            async for event in team.run_stream(
                task=task,
                cancellation_token=cancellation_token,
            ):
                if cancellation_token and cancellation_token.is_cancelled():
                    break
                yield event
                await tenant_client.event.emit(event)

        finally:
            await tenant_client.ag.save_team_state(
                team=team,
                team_id=team_id,
                tenant_id=tenant_client.tenant_id,
                chat_id=chat_id,
            )
