from typing import AsyncGenerator, List, Sequence

from autogen_agentchat.base import TaskResult
from autogen_agentchat.messages import AgentEvent, ChatMessage
from autogen_core import CancellationToken, Component, ComponentModel
from loguru import logger
from mtmai.agents.tenant_agent.tenant_agent import MsgResetTenant
from mtmai.context.context_client import TenantClient
from mtmai.context.ctx import get_chat_session_id_ctx, get_team_id_ctx
from mtmai.mtlibs.id import generate_uuid
from mtmai.mtmpb.events_pb2 import ChatSessionStartEvent
from mtmai.teams.base_team import MtBaseTeam
from pydantic import BaseModel


class TeamTeamConfig(BaseModel):
    participants: List[ComponentModel]
    termination_condition: ComponentModel | None = None
    max_turns: int | None = None


class TeamTeam(MtBaseTeam, Component[TeamTeamConfig]):
    component_type = "mtmai.teams.team_team.TeamTeam"

    def __init__(self):
        super().__init__()

    async def run_stream(
        self,
        *,
        task: str | ChatMessage | Sequence[ChatMessage] | None = None,
        cancellation_token: CancellationToken | None = None,
    ) -> AsyncGenerator[AgentEvent | ChatMessage | TaskResult, None]:
        tenant_client = TenantClient()
        if task.startswith("/tenant/seed"):
            logger.info("通知 TanantAgent 初始化(或重置)租户信息")
            result = await self._runtime.send_message(
                MsgResetTenant(tenant_id=tenant_client.tenant_id),
                self.tenant_agent_id,
            )
            return

        team_id = get_team_id_ctx()
        tenant_id = tenant_client.tenant_id
        if not team_id:
            tenant_teams = await tenant_client.ag.list_team_component(tenant_id)
            logger.info(f"get team component: {tenant_teams}")
            team_id = tenant_teams[0].metadata.id

        team = await tenant_client.ag.get_team(tenant_client.tenant_id, team_id)
        if not team_id:
            team_id = generate_uuid()

        chat_session_id = get_chat_session_id_ctx()
        # TODO: 获取 session state, 如果获取失败,触发 ChatSessionStartEvent 事件.
        if not chat_session_id:
            chat_session_id = generate_uuid()

        else:
            logger.info(f"现有session: {chat_session_id}")
            # 加载团队状态
            # await self.load_state(thread_id)
            ...

        await tenant_client.emit(
            ChatSessionStartEvent(
                threadId=chat_session_id,
            )
        )

        try:
            async for event in team.run_stream(
                task=task,
                cancellation_token=cancellation_token,
            ):
                if cancellation_token and cancellation_token.is_cancelled():
                    break
                await tenant_client.event.emit(event)

                # if isinstance(event, TaskResult):
                #     logger.info(f"Worker Agent 收到任务结果: {event}")
                #     task_result = event
                # elif isinstance(
                #     event,
                #     (
                #         TextMessage,
                #         MultiModalMessage,
                #         StopMessage,
                #         HandoffMessage,
                #         ToolCallRequestEvent,
                #         ToolCallExecutionEvent,
                #         LLMCallEventMessage,
                #     ),
                # ):
                #     # if event.content:
                #     await tenant_client.ag.handle_message_create(
                #         ChatMessageUpsert(
                #             content=event.content,
                #             tenant_id=tenant_client.tenant_id,
                #             component_id=message.team_id,
                #             threadId=thread_id,
                #             role=event.source,
                #             runId=tenant_client.run_id,
                #             stepRunId=message.step_run_id,
                #         ),
                #     )
                #     await tenant_client.event.stream(
                #         event, step_run_id=message.step_run_id
                #     )
                #     # else:
                #     #     logger.warn(f"worker Agent 消息没有content: {event}")
                # else:
                #     logger.warn(f"worker Agent 收到(未知类型)消息: {event}")
        finally:
            await tenant_client.ag.save_team_state(
                team=team,
                team_id=team_id,
                tenant_id=tenant_client.tenant_id,
                run_id=tenant_client.run_id,
            )
