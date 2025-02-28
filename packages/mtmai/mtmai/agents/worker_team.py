from __future__ import annotations

import json

from autogen_agentchat.base import TaskResult, Team
from autogen_agentchat.messages import (
    HandoffMessage,
    MultiModalMessage,
    StopMessage,
    TextMessage,
    ToolCallExecutionEvent,
    ToolCallRequestEvent,
)
from autogen_core import CancellationToken, SingleThreadedAgentRuntime
from autogenstudio.datamodel import LLMCallEventMessage
from connecpy.context import ClientContext
from loguru import logger
from opentelemetry.trace import TracerProvider

from mtmai.agents.tenant_agent.tenant_agent import MsgResetTenant
from mtmai.clients.rest.models.agent_run_input import AgentRunInput
from mtmai.clients.rest.models.chat_message_upsert import ChatMessageUpsert
from mtmai.clients.rest.models.mt_component import MtComponent
from mtmai.context.context import Context
from mtmai.mtlibs.id import generate_uuid
from mtmai.mtmpb import ag_pb2
from mtmai.mtmpb.events_pb2 import ChatSessionStartEvent


class WorkerTeam:
    def __init__(
        self,
        hatctx: Context,
        tracer_provider: TracerProvider | None = None,
    ) -> None:
        self.hatctx = hatctx
        # self._runtime = hatctx.agent_runtime
        # if not self._runtime:
        self._runtime = SingleThreadedAgentRuntime(
            tracer_provider=tracer_provider,
            # payload_serialization_format=self._payload_serialization_format,
        )

        # self._runtime = MtmAgentRuntime(agent_rpc_client=hatctx.aio.ag)

        self.cancellation_token = CancellationToken()

    async def run(self, message: AgentRunInput) -> TaskResult:
        tenant_id: str | None = message.tenant_id
        run_id = message.run_id
        user_input = message.content
        if user_input.startswith("/tenant/seed"):
            logger.info(f"通知 TanantAgent 初始化(或重置)租户信息: {message}")
            result = await self._runtime.send_message(
                MsgResetTenant(tenant_id=tenant_id),
                self.tenant_agent_id,
            )
            return

        # self._runtime = MtmAgentRuntime(agent_rpc_client=self.hatctx.aio.ag)

        # rpc_demo_team = RpcDemoTeam(self._runtime)
        # await rpc_demo_team.run()

        team_comp_data: MtComponent = None
        if not message.team_id:
            # team_id = "fake_team_id"
            # result = await self._runtime.send_message(
            #     MsgGetTeamComponent(tenant_id=message.tenant_id, component_id=team_id),
            #     self.tenant_agent_id,
            # )
            tenant_teams = await self.hatctx.ag_client2.list_team_component(
                message.tenant_id
            )
            logger.info(f"get team component: {tenant_teams}")
            message.team_id = tenant_teams[0].metadata.id

        team_comp_data = await self.hatctx.ag.GetComponent(
            ctx=ClientContext(),
            request=ag_pb2.GetComponentReq(
                tenant_id=message.tenant_id, component_id=message.team_id
            ),
        )

        component_json = json.loads(team_comp_data.component)

        team = Team.load_component(component_json)
        team_id = message.team_id
        if not team_id:
            team_id = generate_uuid()

        thread_id = message.session_id
        # TODO: 获取 session state, 如果获取失败,触发 ChatSessionStartEvent 事件.
        if not thread_id:
            thread_id = generate_uuid()

        else:
            logger.info(f"现有session: {thread_id}")
            # 加载团队状态
            # await self.load_state(thread_id)
            ...

        step_run_id = self.hatctx.step_run_id
        await self.hatctx.event.stream(
            step_run_id=step_run_id,
            data=ChatSessionStartEvent(
                threadId=thread_id,
            ),
        )

        task_result: TaskResult | None = None
        try:
            async for event in team.run_stream(
                task=message.content,
                cancellation_token=self.cancellation_token,
            ):
                if self.cancellation_token and self.cancellation_token.is_cancelled():
                    break

                if isinstance(event, TaskResult):
                    logger.info(f"Worker Agent 收到任务结果: {event}")
                    task_result = event
                elif isinstance(
                    event,
                    (
                        TextMessage,
                        MultiModalMessage,
                        StopMessage,
                        HandoffMessage,
                        ToolCallRequestEvent,
                        ToolCallExecutionEvent,
                        LLMCallEventMessage,
                    ),
                ):
                    if event.content:
                        await self.hatctx.ag_client2.handle_message_create(
                            ChatMessageUpsert(
                                content=event.content,
                                tenant_id=message.tenant_id,
                                component_id=message.team_id,
                                threadId=thread_id,
                                role=event.source,
                                runId=run_id,
                                stepRunId=message.step_run_id,
                            ),
                        )
                        await self.hatctx.event.stream(
                            event, step_run_id=message.step_run_id
                        )
                    else:
                        logger.warn(f"worker Agent 消息没有content: {event}")
                else:
                    logger.info(f"worker Agent 收到(未知类型)消息: {event}")
        finally:
            await self.hatctx.ag_client2.save_team_state(
                team=team,
                team_id=team_id,
                tenant_id=tenant_id,
                run_id=run_id,
            )
        return task_result
