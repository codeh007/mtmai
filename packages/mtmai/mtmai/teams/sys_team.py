from abc import ABC
from typing import Any, AsyncGenerator, List, Mapping, Sequence

from autogen_agentchat.base import TaskResult, Team
from autogen_agentchat.messages import AgentEvent, ChatMessage
from autogen_agentchat.state import TeamState
from autogen_core import CancellationToken, Component, ComponentModel
from loguru import logger
from mtmai.agents.tenant_agent.tenant_agent import MsgResetTenant
from mtmai.context.context_client import TenantClient
from mtmai.context.ctx import get_chat_session_id_ctx, get_team_id_ctx
from mtmai.mtlibs.id import generate_uuid
from mtmai.mtmpb.events_pb2 import ChatSessionStartEvent
from pydantic import BaseModel


class SysTeamConfig(BaseModel):
    """The declarative configuration RoundRobinGroupChat."""

    participants: List[ComponentModel]
    termination_condition: ComponentModel | None = None
    max_turns: int | None = None


class SysTeam(Team, ABC, Component[SysTeamConfig]):
    component_type = "mtmai.teams.sys_team.SysTeam"

    def __init__(self):
        super().__init__()

    async def run(
        self,
        *,
        task: str | ChatMessage | Sequence[ChatMessage] | None = None,
        cancellation_token: CancellationToken | None = None,
    ) -> TaskResult:
        async for event in self.run_stream(
            task=task,
            cancellation_token=cancellation_token,
        ):
            result: TaskResult | None = None
            async for message in self.run_stream(
                task=task,
                cancellation_token=cancellation_token,
            ):
                if isinstance(message, TaskResult):
                    result = message
            if result is not None:
                return result
            raise AssertionError("The stream should have returned the final result.")

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
        # team_id = team_id
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

        await tenant_client.event.stream(
            step_run_id=tenant_client.step_run_id,
            data=ChatSessionStartEvent(
                threadId=chat_session_id,
            ),
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

    async def reset(self) -> None:
        # if not self._initialized:
        #     await self._init(self._runtime)

        # if self._is_running:
        #     raise RuntimeError("The group chat is currently running. It must be stopped before it can be reset.")
        # self._is_running = True

        # # Start the runtime.
        # self._runtime.start()

        # try:
        #     # Send a reset messages to all participants.
        #     for participant_topic_type in self._participant_topic_types:
        #         await self._runtime.send_message(
        #             GroupChatReset(),
        #             recipient=AgentId(type=participant_topic_type, key=self._team_id),
        #         )
        #     # Send a reset message to the group chat manager.
        #     await self._runtime.send_message(
        #         GroupChatReset(),
        #         recipient=AgentId(type=self._group_chat_manager_topic_type, key=self._team_id),
        #     )
        # finally:
        #     # # Stop the runtime.
        #     # await self._runtime.stop_when_idle()

        #     # # Reset the output message queue.
        #     # self._stop_reason = None
        #     # while not self._output_message_queue.empty():
        #     #     self._output_message_queue.get_nowait()

        #     # # Indicate that the team is no longer running.
        #     # self._is_running = False
        ...

    async def save_state(self) -> Mapping[str, Any]:
        """Save the state of the group chat team."""
        if not self._initialized:
            raise RuntimeError(
                "The group chat has not been initialized. It must be run before it can be saved."
            )

        if self._is_running:
            raise RuntimeError("The team cannot be saved while it is running.")
        self._is_running = True

        try:
            # Save the state of the runtime. This will save the state of the participants and the group chat manager.
            agent_states = await self._runtime.save_state()
            return TeamState(
                agent_states=agent_states, team_id=self._team_id
            ).model_dump()
        finally:
            # Indicate that the team is no longer running.
            self._is_running = False

    async def load_state(self, state: Mapping[str, Any]) -> None:
        """Load the state of the group chat team."""
        if not self._initialized:
            await self._init(self._runtime)

        if self._is_running:
            raise RuntimeError("The team cannot be loaded while it is running.")
        self._is_running = True

        try:
            # Load the state of the runtime. This will load the state of the participants and the group chat manager.
            team_state = TeamState.model_validate(state)
            self._team_id = team_state.team_id
            await self._runtime.load_state(team_state.agent_states)
        finally:
            # Indicate that the team is no longer running.
            self._is_running = False
