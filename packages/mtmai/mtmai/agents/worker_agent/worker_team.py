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
from autogen_core import AgentRuntime, SingleThreadedAgentRuntime
from autogenstudio.datamodel import LLMCallEventMessage
from connecpy.context import ClientContext
from loguru import logger
from mtmai.agents.model_client import MtmOpenAIChatCompletionClient
from mtmai.agents.team_builder.article_gen_teambuilder import ArticleGenTeamBuilder
from mtmai.agents.team_builder.assisant_team_builder import AssistantTeamBuilder
from mtmai.agents.team_builder.m1_web_builder import M1WebTeamBuilder
from mtmai.agents.team_builder.swram_team_builder import SwramTeamBuilder
from mtmai.agents.team_builder.travel_builder import TravelTeamBuilder
from mtmai.agents.tenant_agent.tenant_agent import MsgResetTenant
from mtmai.clients.rest.models.ag_state_upsert import AgStateUpsert
from mtmai.clients.rest.models.agent_run_input import AgentRunInput
from mtmai.clients.rest.models.chat_message_upsert import ChatMessageUpsert
from mtmai.clients.rest.models.mt_component import MtComponent
from mtmai.context.context import Context
from mtmai.mtlibs.id import generate_uuid
from mtmai.mtmpb import ag_pb2
from opentelemetry.trace import TracerProvider


class WorkerTeam:
    def __init__(
        self,
        hatctx: Context,
        runtime: AgentRuntime = None,
        tracer_provider: TracerProvider | None = None,
        # payload_serialization_format: str = JSON_DATA_CONTENT_TYPE,
    ) -> None:
        self.hatctx = hatctx
        # self.client = client
        # self.rest = hatctx.aio
        # self._trace_helper = TraceHelper(
        #     tracer_provider, MessageRuntimeTracingConfig("Worker Runtime")
        # )
        # self._per_type_subscribers: DefaultDict[tuple[str, str], Set[AgentId]] = (
        #     defaultdict(set)
        # )
        # self._agent_factories: Dict[
        #     str,
        #     Callable[[], Agent | Awaitable[Agent]]
        #     | Callable[[AgentRuntime, AgentId], Agent | Awaitable[Agent]],
        # ] = {}
        # self._instantiated_agents: Dict[AgentId, Agent] = {}
        # self._known_namespaces: set[str] = set()
        # self._read_task: None | Task[None] = None
        # self._running = False
        # self._pending_requests: Dict[str, Future[Any]] = {}
        # self._pending_requests_lock = asyncio.Lock()
        # self._next_request_id = 0
        # self._background_tasks: Set[Task[Any]] = set()
        # self._subscription_manager = SubscriptionManager()
        # self._serialization_registry = SerializationRegistry()

        # if payload_serialization_format not in {
        #     JSON_DATA_CONTENT_TYPE,
        #     PROTOBUF_DATA_CONTENT_TYPE,
        # }:
        #     raise ValueError(
        #         f"Unsupported payload serialization format: {payload_serialization_format}"
        #     )

        # self._payload_serialization_format = payload_serialization_format
        self._runtime = runtime
        if not self._runtime:
            self._runtime = SingleThreadedAgentRuntime(
                tracer_provider=tracer_provider,
                # payload_serialization_format=self._payload_serialization_format,
            )

    async def handle_message(self, message: AgentRunInput) -> TaskResult:
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
        team_comp_data: MtComponent = None
        if not message.team_id:
            # team_id = "fake_team_id"
            # result = await self._runtime.send_message(
            #     MsgGetTeamComponent(tenant_id=message.tenant_id, component_id=team_id),
            #     self.tenant_agent_id,
            # )
            tenant_teams = await self.list_team_component(message.tenant_id)
            logger.info(f"get team component: {tenant_teams}")
            message.team_id = tenant_teams[0].metadata.id

        team_comp_data = await self.client.ag.GetComponent(
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
        if not thread_id:
            thread_id = generate_uuid()
        else:
            logger.info(f"现有session: {thread_id}")
            # 加载团队状态
            # await self.load_state(thread_id)
            ...

        task_result: TaskResult | None = None
        try:
            async for event in team.run_stream(
                task=message.content,
                # cancellation_token=ctx.cancellation_token,
            ):
                # if ctx.cancellation_token and ctx.cancellation_token.is_cancelled():
                #     break

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
                        await self.handle_message_create(
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
                        await self.client.event.stream(
                            "hello1await22222222", step_run_id=message.step_run_id
                        )
                    else:
                        logger.warn(f"worker Agent 消息没有content: {event}")
                else:
                    logger.info(f"worker Agent 收到(未知类型)消息: {event}")
        finally:
            await self.save_team_state(
                team=team,
                team_id=team_id,
                tenant_id=tenant_id,
                run_id=run_id,
            )
        return task_result

    async def list_team_component(self, tenant_id: str):
        return await self.tenant_reset_teams(tenant_id)

    async def tenant_reset_teams(self, tenant_id: str):
        logger.info(f"TenantAgent 重置租户信息: {tenant_id}")
        results = []
        teams_list = await self.hatctx.aio.rest_client.aio.coms_api.coms_list(
            tenant=tenant_id, label="default"
        )
        if teams_list.rows and len(teams_list.rows) > 0:
            logger.info(f"获取到默认聊天团队 {teams_list.rows[0].metadata.id}")
            results.append(teams_list.rows[0])
        defaultModel = await self.rest.model_api.model_get(
            tenant=tenant_id, model="default"
        )
        model_dict = defaultModel.config.model_dump()
        model_dict.pop("n", None)
        model_client = MtmOpenAIChatCompletionClient(
            **model_dict,
        )

        self.team_builders = [
            AssistantTeamBuilder(),
            SwramTeamBuilder(),
            ArticleGenTeamBuilder(),
            M1WebTeamBuilder(),
            TravelTeamBuilder(),
        ]
        for team_builder in self.team_builders:
            label = team_builder.name
            logger.info(f"create team for tenant {tenant_id}")
            team_comp = await team_builder.create_team(model_client)
            component_model = team_comp.dump_component()
            new_team = await self.hatctx.aio.rest_client.aio.coms_api.coms_upsert(
                tenant=tenant_id,
                com=generate_uuid(),
                mt_component=MtComponent(
                    label=label,
                    description=component_model.description or "",
                    componentType="team",
                    component=component_model.model_dump(),
                ).model_dump(),
            )
            results.append(new_team)
        return results

    async def save_team_state(
        self, team: Team, team_id: str, tenant_id: str, run_id: str
    ) -> None:
        """保存团队状态"""
        logger.info("保存团队状态")
        # 确保停止团队的内部 agents
        if team and hasattr(team, "_participants"):
            for agent in team._participants:
                if hasattr(agent, "close"):
                    await agent.close()
        state = await team.save_state()
        await self.hatctx.aio.rest_client.aio.ag_state_api.ag_state_upsert(
            tenant=tenant_id,
            ag_state_upsert=AgStateUpsert(
                componentId=team_id,
                runId=run_id,
                state=state,
            ).model_dump(),
        )

    async def handle_message_create(self, message: ChatMessageUpsert) -> None:
        await self.hatctx.aio.rest_client.aio.chat_api.chat_message_upsert(
            tenant=message.tenant_id,
            chat_message_upsert=message.model_dump(),
        )
