import inspect

from autogen_agentchat.base import TaskResult, Team
from autogen_core import AgentRuntime, MessageContext, RoutedAgent, message_handler
from autogen_core.models import ChatCompletionClient
from loguru import logger
from mtmai.agents.team_builder import default_team_name
from mtmai.clients.rest.models.chat_session_start_event import ChatSessionStartEvent
from mtmai.clients.rest.models.team_runner_task import TeamRunnerTask
from mtmai.context.context_client import TenantClient
from mtmai.context.ctx import get_tenant_id, set_step_canceled_ctx
from mtmai.teams.instagram_team import InstagramTeam


class TeamRunnerAgent(RoutedAgent):
    def __init__(self, description: str, model_client: ChatCompletionClient) -> None:
        super().__init__(description)
        self._model_client = model_client
        self.teams: list[Team] = []

    # @message_handler
    # async def handle_run_team(
    #     self, message: TeamRunnerTask, ctx: MessageContext
    # ) -> None:
    #     logger.info("(TeamRunnerTask)")
    #     task = message.task
    #     assistant = MtAssistantAgent(
    #         "Assistant",
    #         model_client=self._model_client,
    #     )

    #     surfer = MultimodalWebSurfer(
    #         "WebSurfer",
    #         model_client=self._model_client,
    #     )

    #     team = MagenticOneGroupChat(
    #         [assistant, surfer], model_client=self._model_client
    #     )
    #     await Console(
    #         team.run_stream(task="Provide a different proof for Fermat's Last Theorem")
    #     )

    #     # task = message.task
    #     # team_id = message.team_id
    #     # chat_id = message.chat_id

    #     # logger.info(f"{'-'*80}\nUser login, session ID: {self.id.key}.", flush=True)
    #     # # Get the user's initial input after login.
    #     # user_input = input("User: ")
    #     # logger.info(f"{'-'*80}\n{self.id.type}:\n{user_input}")
    #     # await self.publish_message(
    #     #     UserTask(context=[UserMessage(content=user_input, source="User")]),
    #     #     topic_id=TopicId(self._agent_topic_type, source=self.id.key),
    #     # )

    #     # tenant_client = TenantClient()
    #     # tid = tenant_client.tenant_id
    #     # if task.startswith("/tenant/seed"):
    #     #     logger.info("通知 TanantAgent 初始化(或重置)租户信息")
    #     #     result = await self._runtime.send_message(
    #     #         MsgResetTenant(tenant_id=tid),
    #     #         self.tenant_agent_id,
    #     #     )
    #     #     return

    #     # team_id = get_team_id_ctx() or generate_uuid()
    #     # chat_id = get_chat_session_id_ctx() or generate_uuid()
    #     # team = await tenant_client.ag.get_team()
    #     # ag_state = await tenant_client.ag.load_team_state(
    #     #     tenant_id=tenant_client.tenant_id,
    #     #     chat_id=chat_id,
    #     # )
    #     # if ag_state:
    #     #     await team.load_state(ag_state.state)

    #     # logger.info(f"运行: task: {task}, chat_id:{chat_id}")

    #     # await tenant_client.emit(
    #     #     ChatSessionStartEvent(
    #     #         threadId=chat_id,
    #     #     )
    #     # )

    #     # try:
    #     #     async for event in team.run_stream(
    #     #         task=task,
    #     #         cancellation_token=ctx.cancellation_token,
    #     #     ):
    #     #         if ctx.cancellation_token and ctx.cancellation_token.is_cancelled():
    #     #             break
    #     #         # yield event
    #     #         await tenant_client.event.emit(event)

    #     # finally:
    #     #     await tenant_client.ag.save_team_state(
    #     #         team=team,
    #     #         team_id=team_id,
    #     #         tenant_id=tenant_client.tenant_id,
    #     #         chat_id=chat_id,
    #     #     )

    #     # return

    @message_handler
    async def run_team(self, message: TeamRunnerTask, ctx: MessageContext) -> None:
        logger.info(f"(TeamRunnerTask), resource_id: {message.resource_id}")
        set_step_canceled_ctx(False)
        tenant_client = TenantClient()
        # team = await tenant_client.ag.get_team_by_resource(
        #     # cancellation_token=cancellation_token,
        #     resource_id=message.resource_id,
        # )
        session_id = self.id.key

        team = await self.build_team(
            runtime=self._runtime, component_id_or_name=message.resource_id
        )
        await tenant_client.emit(ChatSessionStartEvent(threadId=session_id))
        self.teams.append(team)

        stream = team.run_stream(
            task=message.content,
            cancellation_token=ctx.cancellation_token,
        )
        if inspect.isawaitable(stream):
            stream = await stream

        async for event in stream:
            if ctx.cancellation_token and ctx.cancellation_token.is_cancelled():
                break
            if isinstance(event, TaskResult):
                return event
            await tenant_client.emit(event)

    async def build_team(
        self, runtime: AgentRuntime, component_id_or_name: str | None = None
    ):
        tenant_client = TenantClient()
        tid = get_tenant_id()
        if not tid:
            raise ValueError("tenant_id is required")
        if not component_id_or_name:
            component_id_or_name = default_team_name
        model_client = await tenant_client.ag.default_model_client(tid)

        resource_data = await tenant_client.ag.resource_api.resource_get(
            tenant=tid,
            resource=component_id_or_name,
        )

        # 方式1
        # team_builder = resource_team_map.get(resource_data.type)
        # if not team_builder:
        #     raise ValueError(
        #         f"cant create team for unsupported resource type: {resource_data.type}"
        #     )
        # team = await team_builder.create_team(
        #     runtime=runtime, model_client=model_client
        # )

        # 方式2
        team = InstagramTeam(
            participants=[],
            model_client=model_client,
            # termination_condition=None,
            # max_turns=None,
            runtime=runtime,
        )

        return team
