from abc import ABC
from typing import AsyncGenerator, List, Sequence

from autogen_agentchat.base import TaskResult, Team, TerminationCondition
from autogen_agentchat.messages import AgentEvent, ChatMessage
from autogen_core import CancellationToken, Component, ComponentModel
from loguru import logger
from pydantic import BaseModel

from ..agents.tenant_agent.tenant_agent import MsgResetTenant
from ..context.context_client import TenantClient
from ..context.ctx import get_chat_session_id_ctx, get_team_id_ctx
from ..mtlibs.id import generate_uuid
from ..mtmpb.events_pb2 import ChatSessionStartEvent

# class MtAssisantTeamManager(BaseGroupChatManager):
#     """A group chat manager that selects the next speaker in a round-robin fashion."""

#     def __init__(
#         self,
#         group_topic_type: str,
#         output_topic_type: str,
#         participant_topic_types: List[str],
#         participant_descriptions: List[str],
#         termination_condition: TerminationCondition | None,
#         max_turns: int | None = None,
#     ) -> None:
#         super().__init__(
#             group_topic_type,
#             output_topic_type,
#             participant_topic_types,
#             participant_descriptions,
#             termination_condition,
#             max_turns,
#         )
#         self._next_speaker_index = 0

#     async def validate_group_state(self, messages: List[ChatMessage] | None) -> None:
#         pass

#     async def reset(self) -> None:
#         self._current_turn = 0
#         self._message_thread.clear()
#         if self._termination_condition is not None:
#             await self._termination_condition.reset()
#         self._next_speaker_index = 0

#     async def save_state(self) -> Mapping[str, Any]:
#         state = RoundRobinManagerState(
#             message_thread=list(self._message_thread),
#             current_turn=self._current_turn,
#             next_speaker_index=self._next_speaker_index,
#         )
#         return state.model_dump()

#     async def load_state(self, state: Mapping[str, Any]) -> None:
#         round_robin_state = RoundRobinManagerState.model_validate(state)
#         self._message_thread = list(round_robin_state.message_thread)
#         self._current_turn = round_robin_state.current_turn
#         self._next_speaker_index = round_robin_state.next_speaker_index

#     async def select_speaker(self, thread: List[AgentEvent | ChatMessage]) -> str:
#         """Select a speaker from the participants in a round-robin fashion."""
#         current_speaker_index = self._next_speaker_index
#         self._next_speaker_index = (current_speaker_index + 1) % len(
#             self._participant_topic_types
#         )
#         current_speaker = self._participant_topic_types[current_speaker_index]
#         return current_speaker


class MtAssisantTeamConfig(BaseModel):
    """The declarative configuration RoundRobinGroupChat."""

    participants: List[ComponentModel]
    termination_condition: ComponentModel | None = None
    max_turns: int | None = None


class MtAssisantTeam(Team, ABC, Component[MtAssisantTeamConfig]):
    # component_config_schema = MtAssisantTeamConfig
    component_type = "mtmai.teams.MtAssisantTeam"

    def __init__(
        self,
        # participants: List[ChatAgent],
        termination_condition: TerminationCondition | None = None,
        max_turns: int | None = None,
    ):
        super().__init__(
            # participants,
            # group_chat_manager_class=MtAssisantTeamManager,
            # termination_condition=termination_condition,
            # max_turns=max_turns,
        )

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

        thread_id = get_chat_session_id_ctx()
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
