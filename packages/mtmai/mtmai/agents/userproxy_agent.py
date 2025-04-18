from textwrap import dedent
from typing import (
    Any,
    AsyncGenerator,
    Awaitable,
    Callable,
    Mapping,
    Optional,
    Sequence,
    Union,
    cast,
)

from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.agents import UserProxyAgent as AutoGenUserProxyAgent
from autogen_agentchat.base import Response
from autogen_agentchat.messages import BaseAgentEvent, BaseChatMessage, TextMessage
from autogen_core import (
    CancellationToken,
    Component,
    DefaultTopicId,
    FunctionCall,
    MessageContext,
    message_handler,
)
from autogen_core.model_context import BufferedChatCompletionContext
from autogen_core.models import (
    AssistantMessage,
    FunctionExecutionResultMessage,
    LLMMessage,
    SystemMessage,
    UserMessage,
)
from autogen_core.tools import Tool
from autogen_ext.code_executors.docker import DockerCommandLineCodeExecutor
from autogen_ext.tools.code_execution import PythonCodeExecutionTool
from loguru import logger
from mtmai.clients.rest.models.agent_topic_types import AgentTopicTypes
from mtmai.clients.rest.models.ask_user_function_call import AskUserFunctionCall
from mtmai.clients.rest.models.assistant_message import (
    AssistantMessage as MtAssistantMessage,
)
from mtmai.clients.rest.models.chat_message_input import ChatMessageInput
from mtmai.clients.rest.models.chat_message_upsert import ChatMessageUpsert
from mtmai.clients.rest.models.chat_start_input import ChatStartInput
from mtmai.clients.rest.models.flow_login_result import FlowLoginResult
from mtmai.clients.rest.models.flow_names import FlowNames
from mtmai.clients.rest.models.form_field import FormField
from mtmai.clients.rest.models.mt_llm_message import MtLlmMessage
from mtmai.clients.rest.models.mt_llm_message_types import MtLlmMessageTypes
from mtmai.clients.rest.models.social_login_input import SocialLoginInput
from mtmai.clients.rest.models.user_agent_state import UserAgentState
from mtmai.clients.rest.models.user_proxy_agent_config import UserProxyAgentConfig
from mtmai.mtlibs.id import generate_uuid
from typing_extensions import Self

SyncInputFunc = Callable[[str], str]
AsyncInputFunc = Callable[[str, Optional[CancellationToken]], Awaitable[str]]
InputFuncType = Union[SyncInputFunc, AsyncInputFunc]


class UserProxyAgent(AutoGenUserProxyAgent, Component[UserProxyAgentConfig]):
    component_type = "agent"
    component_provider_override = "mtmai.agents.userproxy_agent.UserProxyAgent"
    component_config_schema = UserProxyAgentConfig

    def __init__(
        self,
        name: str,
        *,
        description: str = "A human user",
        input_func: Optional[InputFuncType] = None,
    ) -> None:
        super().__init__(name=name, description=description, input_func=input_func)

    # def weather_tool(self):
    #     def get_weather(city: str) -> str:
    #         return "sunny"

    #     return FunctionTool(get_weather, description="Get the weather of a city.")

    # def social_login_tool(self):
    #     def social_login() -> str:
    #         json1 = SocialLoginInput(
    #             type="SocialLoginInput",
    #             username="username1",
    #             password="password1",
    #             otp_key="",
    #         ).model_dump_json()
    #         return json1

    #     return FunctionTool(
    #         social_login,
    #         description="Social login tool. 登录第三方社交媒体, 例如: instagram, twitter, tiktok, etc.",
    #     )

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

        assistant = AssistantAgent(
            "assistant",
            model_client=self.model_client,
            model_context=self._state.model_context,
            tools=await self.get_tools(ctx),
            system_message=dedent(
                "你是实用助手,需要使用提供的工具解决用户提出的问题"
                "重要:"
                "1. 当用户明确调用 登录工具时才调用 登录工具"
                "2. 当用户明确调用 获取天气工具时才调用 获取天气工具"
            ),
        )

        response = await assistant.on_messages(
            [TextMessage(content=message.content, source="user")],
            ctx.cancellation_token,
        )
        await self.add_chat_message(
            ctx,
            AssistantMessage(
                content=response.chat_message.content,
                source=response.chat_message.source,
            ),
        )
        await self.publish_message(
            response,
            topic_id=DefaultTopicId(
                type=AgentTopicTypes.RESPONSE.value, source=ctx.topic_id.source
            ),
        )

    @message_handler
    async def on_AskUserFunctionCallInput(
        self, message: AskUserFunctionCall, ctx: MessageContext
    ) -> None:
        logger.info(f"on_AskUserFunctionCallInput: {message}")
        pass

    @message_handler
    async def on_social_login(
        self, message: SocialLoginInput, ctx: MessageContext
    ) -> AssistantMessage:
        """
        TODO: 提供两个选项
        1. 登录新账号
        2. 选择已有账号
        """
        child_flow_ref = await self._hatctx.aio.spawn_workflow(
            FlowNames.SOCIAL,
            input=message.model_dump(),
        )
        result = await child_flow_ref.result()
        flow_result = FlowLoginResult.from_dict(result.get("step0"))

        response = AssistantMessage(
            content=f"成功登录 instagram, id: {flow_result.account_id}",
            source=flow_result.source,
        )
        await self.publish_message(
            response,
            topic_id=DefaultTopicId(
                type=AgentTopicTypes.RESPONSE.value, source=ctx.topic_id.source
            ),
        )
        self._state.model_context.add_message(response)
        return response

    async def save_state(self) -> Mapping[str, Any]:
        # upsert_chat_result = await self.tenant_client.chat_api.chat_session_upsert(
        #     tenant=self.tenant_client.tenant_id,
        #     session=self._session_id,
        #     chat_upsert=ChatUpsert(
        #         title=f"userAgent-{datetime.now().strftime('%m-%d-%H-%M')}",
        #         name="userAgent",
        #         state=self._state.model_dump(),
        #         state_type="UserAgentState",
        #     ).model_dump(),
        # )
        # return self._state.model_dump()
        state = await super().save_state()
        return state

    async def load_state(self, state: Mapping[str, Any]) -> None:
        self._state = UserAgentState.from_dict(state)
        self._state.model_context = BufferedChatCompletionContext(buffer_size=15)
        # 从数据库加载聊天记录
        chat_messages = await self.tenant_client.chat_api.chat_messages_list(
            tenant=self.tenant_client.tenant_id,
            chat=self._session_id,
        )
        for chat_message in chat_messages.rows:
            if chat_message.type.value == MtLlmMessageTypes.USERMESSAGE.value:
                msg = UserMessage.model_validate(
                    chat_message.llm_message.actual_instance.model_dump()
                )
                await self._state.model_context.add_message(msg)
            elif chat_message.type.value == MtLlmMessageTypes.ASSISTANTMESSAGE.value:
                mt_assistant_message = cast(
                    MtAssistantMessage, chat_message.llm_message.actual_instance
                )

                content = mt_assistant_message.content.actual_instance
                if isinstance(content, str):
                    content = content
                else:
                    fc_list = []
                    for item in content:
                        fc = FunctionCall(
                            id=item.id,
                            name=item.name,
                            arguments=item.arguments,
                        )
                        fc_list.append(fc)
                    content = fc_list
                msg = AssistantMessage(
                    content=content,
                    source=mt_assistant_message.source,
                    thought=mt_assistant_message.thought,
                )
                await self._state.model_context.add_message(msg)
            elif chat_message.type.value == MtLlmMessageTypes.SYSTEMMESSAGE.value:
                msg = SystemMessage.model_validate(
                    chat_message.llm_message.actual_instance.model_dump()
                )
                await self._state.model_context.add_message(msg)
            elif (
                chat_message.type.value
                == MtLlmMessageTypes.FUNCTIONEXECUTIONRESULTMESSAGE.value
            ):
                msg = FunctionExecutionResultMessage.model_validate(
                    chat_message.llm_message.actual_instance.model_dump()
                )
                await self._state.model_context.add_message(msg)
            else:
                raise ValueError(
                    f"load_state error, Unknown llm message type: {chat_message.type}"
                )

    async def add_chat_message(
        self,
        ctx: MessageContext,
        message: LLMMessage,
    ):
        await self._state.model_context.add_message(message)
        await self.tenant_client.chat_api.chat_message_upsert(
            tenant=self.tenant_client.tenant_id,
            chat_message_upsert=ChatMessageUpsert(
                type=message.type,
                thread_id=self._session_id,
                content=message.model_dump_json(),  # 可能过时了
                content_type="text",
                llm_message=MtLlmMessage.from_dict(message.model_dump()),
                source=message.source,
                topic=ctx.topic_id.type,
            ).model_dump(),
        )

    async def reset(self) -> None:
        await super().reset()

    # async def validate_group_state(
    #     self, messages: List[BaseChatMessage] | None
    # ) -> None: ...

    async def _get_input(
        self, prompt: str, cancellation_token: Optional[CancellationToken]
    ) -> str:
        # return await super()._get_input(prompt, cancellation_token)
        return "fake_user_input_content_123"

    async def on_messages_stream(
        self, messages: Sequence[BaseChatMessage], cancellation_token: CancellationToken
    ) -> AsyncGenerator[BaseAgentEvent | BaseChatMessage | Response, None]:
        async for message in super().on_messages_stream(messages, cancellation_token):
            yield message

    def _to_config(self) -> UserProxyAgentConfig:
        # TODO: Add ability to serialie input_func
        return UserProxyAgentConfig(
            name=self.name, description=self.description, input_func=None
        )

    @classmethod
    def _from_config(cls, config: UserProxyAgentConfig) -> Self:
        return cls(name=config.name, description=config.description, input_func=None)
