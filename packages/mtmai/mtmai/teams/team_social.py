import asyncio
import logging
from inspect import iscoroutinefunction
from typing import (
    Any,
    AsyncGenerator,
    Awaitable,
    Callable,
    List,
    Mapping,
    Optional,
    Sequence,
    Union,
)

from autogen_agentchat.base import ChatAgent, TaskResult, TerminationCondition
from autogen_agentchat.messages import (
    BaseAgentEvent,
    BaseChatMessage,
    HandoffMessage,
    MessageFactory,
    UserInputRequestedEvent,
)
from autogen_agentchat.messages import TextMessage as AutogenTextMessage
from autogen_agentchat.teams import BaseGroupChat
from autogen_agentchat.teams._group_chat._base_group_chat_manager import (
    BaseGroupChatManager,
)
from autogen_agentchat.teams._group_chat._events import GroupChatTermination
from autogen_core import (
    AgentRuntime,
    CancellationToken,
    Component,
    FunctionCall,
    MessageContext,
    message_handler,
)
from autogen_core.models import AssistantMessage, ChatCompletionClient, UserMessage
from autogen_core.tools import FunctionTool, Tool
from autogen_ext.code_executors.docker import DockerCommandLineCodeExecutor
from autogen_ext.tools.code_execution import PythonCodeExecutionTool
from loguru import logger
from mtmai.clients.rest.models.ag_state_upsert import AgStateUpsert
from mtmai.clients.rest.models.agent_state_types import AgentStateTypes
from mtmai.clients.rest.models.ask_user_function_call import AskUserFunctionCall
from mtmai.clients.rest.models.chat_message_input import ChatMessageInput
from mtmai.clients.rest.models.chat_start_input import ChatStartInput
from mtmai.clients.rest.models.flow_team_input import FlowTeamInput
from mtmai.clients.rest.models.form_field import FormField
from mtmai.clients.rest.models.social_login_input import SocialLoginInput
from mtmai.clients.rest.models.social_team_config import SocialTeamConfig
from mtmai.clients.rest.models.social_team_manager_state import SocialTeamManagerState
from mtmai.clients.rest.models.state_type import StateType
from mtmai.clients.rest.models.text_message import TextMessage
from mtmai.clients.tenant_client import TenantClient
from mtmai.context.ctx import get_chat_session_id_ctx
from mtmai.mtlibs.autogen_utils.component_loader import ComponentLoader
from mtmai.mtlibs.id import generate_uuid
from typing_extensions import Self

TRACE_LOGGER_NAME = "mtmai.teams.team_social"
trace_logger = logging.getLogger(TRACE_LOGGER_NAME)

SyncSelectorFunc = Callable[[Sequence[BaseAgentEvent | BaseChatMessage]], str | None]
AsyncSelectorFunc = Callable[
    [Sequence[BaseAgentEvent | BaseChatMessage]], Awaitable[str | None]
]
SelectorFuncType = Union[SyncSelectorFunc | AsyncSelectorFunc]

SyncCandidateFunc = Callable[[Sequence[BaseAgentEvent | BaseChatMessage]], List[str]]
AsyncCandidateFunc = Callable[
    [Sequence[BaseAgentEvent | BaseChatMessage]], Awaitable[List[str]]
]
CandidateFuncType = Union[SyncCandidateFunc | AsyncCandidateFunc]


class SocialTeamManager(BaseGroupChatManager):
    def __init__(
        self,
        name: str,
        group_topic_type: str,
        output_topic_type: str,
        participant_topic_types: List[str],
        participant_names: List[str],
        participant_descriptions: List[str],
        output_message_queue: asyncio.Queue[
            BaseAgentEvent | BaseChatMessage | GroupChatTermination
        ],
        message_factory: MessageFactory,
        selector_prompt: str | None = None,
        allow_repeated_speaker: bool = False,
        selector_func: Optional[SelectorFuncType] = None,
        max_selector_attempts: int = 10,
        model_client: ChatCompletionClient | None = None,
        max_turns: int | None = None,
        termination_condition: TerminationCondition | None = None,
    ) -> None:
        super().__init__(
            name,
            group_topic_type,
            output_topic_type,
            participant_topic_types,
            participant_names,
            participant_descriptions,
            output_message_queue,
            termination_condition,
            max_turns,
            message_factory,
        )
        self.tenant_client = TenantClient()
        self._model_client = model_client
        self._selector_prompt = selector_prompt
        self._previous_speaker: str | None = None
        self._allow_repeated_speaker = allow_repeated_speaker
        self._selector_func = selector_func
        self._is_selector_func_async = iscoroutinefunction(self._selector_func)
        self._max_selector_attempts = max_selector_attempts
        # self._candidate_func = candidate_func
        self._is_candidate_func_async = iscoroutinefunction(self._candidate_func)

        self._state = SocialTeamManagerState(
            type=AgentStateTypes.SOCIALTEAMMANAGERSTATE.value,
            next_speaker_index=0,
            previous_speaker=None,
            current_speaker=self._participant_names[0],
        )
        # self._state.model_context = BufferedChatCompletionContext(buffer_size=15)

    async def _candidate_func(
        self, messages: List[BaseChatMessage] | None
    ) -> List[str]:
        return []

    async def validate_group_state(
        self, messages: List[BaseChatMessage] | None
    ) -> None:
        pass

    def weather_tool(self):
        def get_weather(city: str) -> str:
            return "sunny"

        return FunctionTool(get_weather, description="Get the weather of a city.")

    async def select_speaker(
        self, thread: List[BaseAgentEvent | BaseChatMessage]
    ) -> str:
        """Select a speaker from the participants in a round-robin fashion."""
        self._state.next_speaker_index = (self._state.next_speaker_index + 1) % len(
            self._participant_names
        )
        current_speaker = self._participant_names[self._state.next_speaker_index]
        return current_speaker

    def social_login_tool(self):
        def social_login() -> str:
            json1 = SocialLoginInput(
                type="SocialLoginInput",
                username="username1",
                password="password1",
                otp_key="",
            ).model_dump_json()
            return json1

        return FunctionTool(
            social_login,
            description="Social login tool. 登录第三方社交媒体, 例如: instagram, twitter, tiktok, etc.",
        )

    async def code_execution_tool(self):
        code_executor = DockerCommandLineCodeExecutor()
        await code_executor.start()
        code_execution_tool = PythonCodeExecutionTool(code_executor)
        return code_execution_tool

    async def get_tools(self, ctx: MessageContext) -> list[Tool]:
        tools: list[Tool] = []
        tools.append(await self.code_execution_tool())
        tools.append(self.weather_tool())
        tools.append(self.social_login_tool())
        return tools

    @message_handler
    async def handle_user_input(
        self, message: ChatStartInput, ctx: MessageContext
    ) -> None:
        """对话开始"""
        logger.info(f"handle_agent_run_input: {message}")

    @message_handler
    async def handle_chat_start(
        self, message: ChatMessageInput, ctx: MessageContext
    ) -> None:
        """用户跟聊天助手的对话"""
        logger.info(f"handle_agent_run_input: {message}")

        if not self._state.platform_account_id:
            # 显示 社交媒体登录框
            await self.add_chat_message(
                ctx,
                AssistantMessage(
                    source="assistant",
                    content=[
                        FunctionCall(
                            id=generate_uuid(),
                            name="ask_user",
                            arguments=AskUserFunctionCall(
                                type="AskUserFunctionCall",
                                id=generate_uuid(),
                                title="请选择一个社交媒体账号登录",
                                description="请选择一个社交媒体账号登录",
                                fields=[
                                    FormField(
                                        type="text",
                                        name="username",
                                        label="用户名",
                                        placeholder="请输入用户名",
                                    )
                                ],
                            ).model_dump_json(),
                        )
                    ],
                ),
            )
            return

        await self.add_chat_message(
            ctx, UserMessage(content=message.content, source="user")
        )

        # response = await assistant.on_messages(
        #     [TextMessage(content=message.content, source="user")],
        #     ctx.cancellation_token,
        # )
        # await self.add_chat_message(
        #     ctx,
        #     AssistantMessage(
        #         content=response.chat_message.content,
        #         source=response.chat_message.source,
        #     ),
        # )
        # await self.publish_message(
        #     response,
        #     topic_id=DefaultTopicId(
        #         type=AgentTopicTypes.RESPONSE.value, source=ctx.topic_id.source
        #     ),
        # )

    # @message_handler
    # async def on_AskUserFunctionCallInput(
    #     self, message: AskUserFunctionCall, ctx: MessageContext
    # ) -> None:
    #     logger.info(f"on_AskUserFunctionCallInput: {message}")

    # @message_handler
    # async def on_social_login(
    #     self, message: SocialLoginInput, ctx: MessageContext
    # ) -> AssistantMessage:
    #     """
    #     TODO: 提供两个选项
    #     1. 登录新账号
    #     2. 选择已有账号
    #     """
    #     child_flow_ref = await self._hatctx.aio.spawn_workflow(
    #         FlowNames.SOCIAL,
    #         input=message.model_dump(),
    #     )
    #     result = await child_flow_ref.result()
    #     flow_result = FlowLoginResult.from_dict(result.get("step0"))

    #     response = AssistantMessage(
    #         content=f"成功登录 instagram, id: {flow_result.account_id}",
    #         source=flow_result.source,
    #     )
    #     await self.publish_message(
    #         response,
    #         topic_id=DefaultTopicId(
    #             type=AgentTopicTypes.RESPONSE.value, source=ctx.topic_id.source
    #         ),
    #     )
    #     self._state.model_context.add_message(response)
    #     return response

    async def save_state(self) -> Mapping[str, Any]:
        message_thread = [msg.dump() for msg in self._message_thread]
        state = SocialTeamManagerState(
            type=AgentStateTypes.SOCIALTEAMMANAGERSTATE.value,
            next_speaker_index=self._state.next_speaker_index,
            previous_speaker=self._state.previous_speaker,
            current_speaker=self._state.current_speaker,
            message_thread=message_thread,
            current_turn=self._current_turn,
        )
        return state.model_dump()

    async def load_state(self, state: Mapping[str, Any]) -> None:
        self._state = SocialTeamManagerState.from_dict(state)
        self._message_thread = [
            self._message_factory.create(message)
            for message in self._state.message_thread
        ]
        self._current_turn = self._state.current_turn
        self._current_speaker = self._state.current_speaker
        self._previous_speaker = self._state.previous_speaker

    # async def add_chat_message(
    #     self,
    #     ctx: MessageContext,
    #     message: LLMMessage,
    # ):
    #     await self._state.model_context.add_message(message)
    #     await self.tenant_client.chat_api.chat_message_upsert(
    #         tenant=self.tenant_client.tenant_id,
    #         chat_message_upsert=ChatMessageUpsert(
    #             type=message.type,
    #             thread_id=self._session_id,
    #             content=message.model_dump_json(),  # 可能过时了
    #             content_type="text",
    #             llm_message=MtLlmMessage.from_dict(message.model_dump()),
    #             source=message.source,
    #             topic=ctx.topic_id.type,
    #         ).model_dump(),
    #     )

    async def reset(self) -> None:
        self._current_turn = 0
        self._message_thread.clear()
        if self._termination_condition is not None:
            await self._termination_condition.reset()
        self._previous_speaker = None
        self._state = SocialTeamManagerState(
            type=AgentStateTypes.SOCIALTEAMMANAGERSTATE.value,
            next_speaker_index=0,
            previous_speaker=None,
        )


class SocialTeam(BaseGroupChat, Component[SocialTeamConfig]):
    component_provider_override = "mtmai.teams.team_social.SocialTeam"
    component_config_schema = SocialTeamConfig

    def __init__(
        self,
        participants: List[ChatAgent],
        *,
        termination_condition: TerminationCondition | None = None,
        max_turns: int | None = 20,
        runtime: AgentRuntime | None = None,
        enable_swarm: bool = False,
        custom_message_types: List[type[BaseAgentEvent | BaseChatMessage]]
        | None = None,
    ) -> None:
        super().__init__(
            participants,
            group_chat_manager_name="SocialTeamManager",
            group_chat_manager_class=SocialTeamManager,
            termination_condition=termination_condition,
            max_turns=max_turns,
            runtime=runtime,
            custom_message_types=custom_message_types,
        )
        if enable_swarm:
            # The first participant must be able to produce handoff messages.
            first_participant = self._participants[0]
            if HandoffMessage not in first_participant.produced_message_types:
                raise ValueError(
                    "if enable_swarm, The first participant must be able to produce a handoff messages."
                )

    def _create_group_chat_manager_factory(
        self,
        name: str,
        group_topic_type: str,
        output_topic_type: str,
        participant_topic_types: List[str],
        participant_names: List[str],
        participant_descriptions: List[str],
        output_message_queue: asyncio.Queue[
            BaseAgentEvent | BaseChatMessage | GroupChatTermination
        ],
        termination_condition: TerminationCondition | None,
        max_turns: int | None,
        message_factory: MessageFactory,
    ) -> Callable[[], SocialTeamManager]:
        def _factory() -> SocialTeamManager:
            return SocialTeamManager(
                name=name,
                group_topic_type=group_topic_type,
                output_topic_type=output_topic_type,
                participant_topic_types=participant_topic_types,
                participant_names=participant_names,
                participant_descriptions=participant_descriptions,
                output_message_queue=output_message_queue,
                termination_condition=termination_condition,
                max_turns=max_turns,
                message_factory=message_factory,
            )

        return _factory

    async def reset(self) -> None:
        # self._is_running = False
        await super().reset()

    async def save_state(self) -> Mapping[str, Any]:
        return await super().save_state()

    async def load_state(self, state: Mapping[str, Any]) -> None:
        # await self._runtime.load_state(state)
        await super().load_state(state)

    def _to_config(self) -> SocialTeamConfig:
        return SocialTeamConfig(
            max_turns=self._max_turns,
            enable_swarm=self._enable_swarm,
        )

    @classmethod
    def _from_config(cls, config: SocialTeamConfig) -> Self:
        participants = [
            ComponentLoader.load_component(participant, expected=ChatAgent)
            for participant in config.participants
        ]
        termination_condition = (
            ComponentLoader.load_component(
                config.termination_condition, expected=TerminationCondition
            )
            if config.termination_condition
            else None
        )
        return cls(
            participants,
            termination_condition=termination_condition,
            max_turns=config.max_turns,
            enable_swarm=config.enable_swarm,
        )

    async def pause(self) -> None:
        raise NotImplementedError("TODO: pause team")

    async def resume(self) -> None:
        raise NotImplementedError("TODO: resume team")

    # async def run(
    #     self,
    #     *,
    #     task: str
    #     | BaseChatMessage
    #     | Sequence[BaseChatMessage]
    #     | FlowTeamInput
    #     | None = None,
    #     cancellation_token: CancellationToken | None = None,
    # ) -> TaskResult:
    #     result: TaskResult | None = None
    #     is_slow_user_input = False
    #     async for message in self.run_stream(
    #         task=task,
    #         cancellation_token=cancellation_token,
    #     ):
    #         if isinstance(message, TaskResult):
    #             result = message
    #         elif isinstance(message, UserInputRequestedEvent):
    #             # 强制停止运行, 登录用户的输入(在下一轮中启动)
    #             self._is_running = False
    #             is_slow_user_input = True
    #             await self._runtime.stop()
    #             break
    #     state = await self.save_state()
    #     session_id = get_chat_session_id_ctx()
    #     tenant_client = TenantClient()
    #     await tenant_client.ag_state_api.ag_state_upsert(
    #         tenant=tenant_client.tenant_id,
    #         ag_state_upsert=AgStateUpsert(
    #             type=StateType.TEAMSTATE.value,
    #             chatId=session_id,
    #             state=state,
    #             topic="default",
    #             source="default",
    #         ),
    #     )

    #     if is_slow_user_input:
    #         return {"result": "wait user input"}

    #     if result is None:
    #         raise RuntimeError("result is None")
    #     return result

    async def persist_team_state(self) -> None:
        state = await self.save_state()
        session_id = get_chat_session_id_ctx()
        tenant_client = TenantClient()
        await tenant_client.ag_state_api.ag_state_upsert(
            tenant=tenant_client.tenant_id,
            ag_state_upsert=AgStateUpsert(
                type=StateType.TEAMSTATE.value,
                chatId=session_id,
                state=state,
                topic="default",
                source="default",
            ),
        )

    async def run_stream(
        self,
        *,
        task: str
        | BaseChatMessage
        | Sequence[BaseChatMessage]
        | FlowTeamInput
        | None = None,
        cancellation_token: CancellationToken | None = None,
    ) -> AsyncGenerator[BaseAgentEvent | BaseChatMessage | TaskResult, None]:
        finnal_task = task
        if isinstance(task, FlowTeamInput):
            input_event = task.task.actual_instance
            if isinstance(input_event, TextMessage):
                if not hasattr(input_event, "metadata"):
                    input_event.metadata = {}
                finnal_task = AutogenTextMessage.model_validate(
                    input_event.model_dump()
                )
        async for message in super().run_stream(
            task=finnal_task,
            cancellation_token=cancellation_token,
        ):
            if isinstance(message, TaskResult):
                result = message
                # state = await self.save_state()
                # session_id = get_chat_session_id_ctx()
                # tenant_client = TenantClient()
                # await tenant_client.ag_state_api.ag_state_upsert(
                #     tenant=tenant_client.tenant_id,
                #     ag_state_upsert=AgStateUpsert(
                #         type=StateType.TEAMSTATE.value,
                #         chatId=session_id,
                #         state=state,
                #         topic="default",
                #         source="default",
                #     ),
                # )
                await self.persist_team_state()
                yield result
                break
            elif isinstance(message, UserInputRequestedEvent):
                # 强制停止运行, 登录用户的输入(在下一轮中启动)
                self._is_running = False
                is_slow_user_input = True
                # await self._runtime.stop()

                await self.persist_team_state()
                yield TaskResult(
                    # type=TaskResultTypes.USERINPUTREQUESTED.value,
                    message=AutogenTextMessage(
                        content="wait user input", source="assistant", metadata={}
                    ),
                    stop_reason="wait user input",
                )
                break
            else:
                yield message
