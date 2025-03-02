from __future__ import annotations

from typing import cast

from autogen_agentchat.base import TaskResult
from autogen_core import CancellationToken, SingleThreadedAgentRuntime
from loguru import logger
from mtmai.agents.tenant_agent.tenant_agent import MsgResetTenant
from mtmai.clients.rest.models.agent_run_input import AgentRunInput
from mtmai.context.context import Context
from mtmai.context.context_client import TenantClient
from mtmai.mtlibs.id import generate_uuid
from mtmai.mtmpb.events_pb2 import ChatSessionStartEvent
from mtmai.worker_app import mtmapp
from opentelemetry.trace import TracerProvider


class MtCancelToken(CancellationToken):
    def __init__(self, hatctx: Context):
        # self.is_cancelled = False
        self.cancellation_token: Context | None = hatctx
        super().__init__()

    def cancel(self):
        if self.cancellation_token:
            return self.cancellation_token.cancel()

    def is_cancelled(self):
        if self.cancellation_token:
            return self.cancellation_token.done()


@mtmapp.workflow(
    name="ag",
    on_events=["ag:run"],
)
class FlowAg:
    def __init__(self, tracer_provider: TracerProvider | None = None) -> None:
        self._runtime = SingleThreadedAgentRuntime(
            tracer_provider=tracer_provider,
            # payload_serialization_format=self._payload_serialization_format,
        )
        logger.info("FlowAg 初始化")

    @mtmapp.step(timeout="60m")
    async def step_entry(self, hatctx: Context):
        input = AgentRunInput.model_validate(hatctx.input)
        message = cast(AgentRunInput, input)
        cancellation_token = MtCancelToken(hatctx)
        tenant_client = TenantClient()
        user_input = message.content
        if user_input.startswith("/tenant/seed"):
            logger.info(f"通知 TanantAgent 初始化(或重置)租户信息: {message}")
            result = await self._runtime.send_message(
                MsgResetTenant(tenant_id=tenant_client.tenant_id),
                self.tenant_agent_id,
            )
            return

        if not message.team_id:
            tenant_teams = await tenant_client.ag.list_team_component(message.tenant_id)
            logger.info(f"get team component: {tenant_teams}")
            message.team_id = tenant_teams[0].metadata.id

        team = await tenant_client.ag.get_team(tenant_client.tenant_id, message.team_id)
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

        await tenant_client.event.stream(
            step_run_id=tenant_client.step_run_id,
            data=ChatSessionStartEvent(
                threadId=thread_id,
            ),
        )

        task_result: TaskResult | None = None
        try:
            async for event in team.run_stream(
                task=message.content,
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
        return task_result
