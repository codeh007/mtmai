from autogen_agentchat.base import TaskResult, Team
from autogen_core import (
    MessageContext,
    RoutedAgent,
    SingleThreadedAgentRuntime,
    message_handler,
)
from autogen_core.models import ChatCompletionClient
from loguru import logger
from mtmai.agents.intervention_handlers import NeedsUserInputHandler
from mtmai.clients.rest.models.agent_run_input import AgentRunInput
from mtmai.clients.rest.models.chat_session_start_event import ChatSessionStartEvent
from mtmai.clients.rest.models.mt_task_result import MtTaskResult
from mtmai.context.context_client import TenantClient
from mtmai.context.ctx import get_tenant_id, set_step_canceled_ctx

from ..clients.rest.models.team_component import TeamComponent


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
    async def run_team(self, message: AgentRunInput, ctx: MessageContext) -> None:
        logger.info(f"(TeamRunnerTask), resource_id: {message.resource_id}")
        set_step_canceled_ctx(False)
        tenant_client = TenantClient()
        session_id = self.id.key

        agState = await tenant_client.ag.load_team_state(
            tenant_id=tenant_client.tenant_id,
            chat_id=session_id,
        )
        logger.info(f"agState: {agState}")
        needs_user_input_handler = NeedsUserInputHandler()
        runtime = SingleThreadedAgentRuntime(
            intervention_handlers=[needs_user_input_handler]
        )
        # user_agent_type = await SlowUserProxyAgent.register(
        #     runtime, "User", lambda: SlowUserProxyAgent("User", "I am a user")
        # )
        # await runtime.add_subscription(
        #     TypeSubscription(
        #         topic_type=user_topic_type, agent_type=user_agent_type.type
        #     )
        # )
        # initial_schedule_assistant_message = AssistantTextMessage(
        #     content="Hi! How can I help you? I can help schedule meetings",
        #     source="User",
        # )
        # scheduling_assistant_agent_type = await SchedulingAssistantAgent.register(
        #     runtime,
        #     scheduling_assistant_topic_type,
        #     lambda: SchedulingAssistantAgent(
        #         "SchedulingAssistant",
        #         description="AI that helps you schedule meetings",
        #         model_client=self._model_client,
        #         initial_message=initial_schedule_assistant_message,
        #     ),
        # )
        # await runtime.add_subscription(
        #     subscription=TypeSubscription(
        #         topic_type=scheduling_assistant_topic_type,
        #         agent_type=scheduling_assistant_agent_type.type,
        #     )
        # )
        # runtime_initiation_message: UserTextMessage | AssistantTextMessage
        # latest_user_input = None
        # if latest_user_input is not None:
        #     runtime_initiation_message = UserTextMessage(
        #         content=latest_user_input, source="User"
        #     )
        # else:
        #     runtime_initiation_message = initial_schedule_assistant_message
        # state = state_persister.load_content()

        # if state:
        #     await runtime.load_state(state)
        # await runtime.publish_message(
        #     message=runtime_initiation_message,
        #     # topic_id=TopicId(type=scheduling_assistant_topic_type, source=session_id),
        #     topic_id=TopicId(type=user_agent_type.type, source=session_id),
        # )

        runtime.start()
        # await runtime.stop_when(
        #     lambda: termination_handler.is_terminated
        #     or needs_user_input_handler.needs_user_input
        # )

        # user_input_needed = None
        # if needs_user_input_handler.user_input_content is not None:
        #     user_input_needed = needs_user_input_handler.user_input_content
        # elif termination_handler.is_terminated:
        #     logger.info("Terminated - ", termination_handler.termination_msg)

        # state_to_persist = await runtime.save_state()
        # state_persister.save_content(state_to_persist)

        # team_id = generate_uuid()
        # await tenant_client.ag.save_team_state(
        #         team=team,
        #         team_id=team_id,
        #         tenant_id=tenant_client.tenant_id,
        #         chat_id=session_id,
        #     )

        # return user_input_needed

        team = await self.build_team(component_id=message.component_id)
        await tenant_client.emit(ChatSessionStartEvent(threadId=session_id))
        self.teams.append(team)

        # stream = team.run_stream(
        #     task=message.content,
        #     cancellation_token=ctx.cancellation_token,
        # )
        # if inspect.isawaitable(stream):
        #     stream = await stream
        # stream = asyncio.ensure_future(
        #     team.run_stream(
        #         task=message.content,
        #         cancellation_token=ctx.cancellation_token,
        #     )
        # )
        # needs_user_input_handler = NeedsUserInputHandler()
        # _runtime = SingleThreadedAgentRuntime(
        #     intervention_handlers=[
        #         needs_user_input_handler,
        #         # termination_handler,
        #     ]
        # )
        # team = InstagramTeam(
        #     participants=[],
        #     model_client=self._model_client,
        #     # termination_condition=None,
        #     # max_turns=None,
        #     # runtime=_runtime,
        # )
        # _runtime.start()
        # return team

        ######################################################################################
        # 提示:
        # 1:团队的结束不等于 runtime 的结束
        # 2: runtime 可以复用
        # 3: 可以使用 外置的 持久 agent 参与到临时组建的团队
        ######################################################################################
        async for event in team.run_stream(
            task=message.content,
            cancellation_token=ctx.cancellation_token,
        ):
            if isinstance(message, TaskResult):
                result = message
                mt_result = MtTaskResult(
                    messages=result.messages,
                    stop_reason=result.stop_reason,
                )
                tenant_client.emit(mt_result)
                break
            await tenant_client.emit(event)

        await tenant_client.ag.save_team_state(
            team=team,
            # team_id=team_id,
            tenant_id=tenant_client.tenant_id,
            chat_id=session_id,
        )

        # async for event in aiter(await stream):
        #     if ctx.cancellation_token and ctx.cancellation_token.is_cancelled():
        #         break
        #     if isinstance(event, TaskResult):
        #         return event
        #     await tenant_client.emit(event)

        # await self._runtime.stop_when(
        #     # lambda: self.termination_handler.is_terminated
        #     # or self.needs_user_input_handler.needs_user_input
        #     lambda: self.needs_user_input_handler.needs_user_input
        # )

        # user_input_needed = None
        # if self.needs_user_input_handler.user_input_content is not None:
        #     user_input_needed = self.needs_user_input_handler.user_input_content
        # elif self.termination_handler.is_terminated:
        #     logger.info("Terminated - ", self.termination_handler.termination_msg)

        # state_to_persist = await self._runtime.save_state()
        # logger.info(f"state_to_persist: {state_to_persist}")
        await runtime.stop_when_idle()
        logger.info("团队运行完全结束")

    async def build_team(self, component_id: str | None = None):
        tenant_client = TenantClient()
        tid = get_tenant_id()
        if not tid:
            raise ValueError("tenant_id is required")
        component_data = await tenant_client.ag.coms_api.coms_get(
            tenant=tid,
            com=component_id,
        )
        logger.info(f"component data: {component_data}")

        if not component_data.component_type == "team":
            raise ValueError(
                f"component type must be team, but got {component_data.component_type}"
            )
        team_component = TeamComponent.model_validate(
            component_data.component.actual_instance
        )
        team_component.config.actual_instance

        team = Team.load_component(team_component)
        return team
