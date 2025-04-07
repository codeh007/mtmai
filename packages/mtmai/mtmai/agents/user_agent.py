from textwrap import dedent
from typing import Any, Mapping

from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.messages import TextMessage
from autogen_core import MessageContext, RoutedAgent, message_handler
from autogen_core.model_context import BufferedChatCompletionContext
from autogen_core.models import AssistantMessage, ChatCompletionClient, UserMessage
from autogen_core.tools import FunctionTool, Tool
from autogen_ext.code_executors.docker import DockerCommandLineCodeExecutor
from autogen_ext.tools.code_execution import PythonCodeExecutionTool
from loguru import logger

from mtmai.clients.rest.models.chat_message_input import ChatMessageInput
from mtmai.clients.rest.models.social_login_input import SocialLoginInput
from mtmai.clients.rest.models.user_agent_state import UserAgentState


class UserAgent(RoutedAgent):
    def __init__(
        self,
        description: str,
        session_id: str,
        model_client: ChatCompletionClient | None = None,
        # social_agent_topic_type: str = None,
    ) -> None:
        super().__init__(description)
        self._model_context = BufferedChatCompletionContext(buffer_size=15)
        self._session_id = session_id
        self.model_client = model_client
        self._state = UserAgentState()

    # @message_handler
    # async def handle_agent_run_input(
    #     self, message: AgentUserInput, ctx: MessageContext
    # ) -> None:
    #     """用户输入"""
    #     if ctx.cancellation_token.is_cancelled():
    #         return

    #     session_id = self.id.key
    #     logger.info(
    #         f"{'-'*80}\nhandle_agent_run_input, session ID: {session_id}. task: {message.content}"
    #     )
    #     user_content = message.content
    #     if user_content.startswith("/test_code"):
    #         await self.runtime.publish_message(
    #             message=CodeWritingTask(
    #                 task="Write a function to find the sum of all even numbers in a list."
    #             ),
    #             topic_id=TopicId(AgentTopicTypes.CODER.value, source=session_id),
    #         )
    #     elif user_content.startswith("/test_open_browser"):
    #         await self.runtime.publish_message(
    #             message=BrowserOpenTask(url="https://playwright.dev/"),
    #             topic_id=TopicId(AgentTopicTypes.BROWSER.value, source=session_id),
    #         )
    #     elif user_content.startswith("/test_browser_task"):
    #         await self.runtime.publish_message(
    #             message=BrowserTask(task="Open an online code editor programiz."),
    #             topic_id=TopicId(AgentTopicTypes.BROWSER.value, source=session_id),
    #         )
    #     elif user_content.startswith("/test/ig"):
    #         agent_id = AgentId(self._social_agent_topic_type, "default")
    #         result = await self._runtime.send_message(
    #             SocialAddFollowersInput(
    #                 username="username1",
    #                 password="password1",
    #                 target_username="target_username1",
    #             ),
    #             agent_id,
    #         )
    #         if isinstance(result, IgLoginRequire):
    #             self.is_waiting_ig_login = True

    #         await self._model_context.add_message(
    #             AssistantMessage(
    #                 content=[
    #                     FunctionCall(
    #                         id=generate_uuid(),
    #                         name="ig_login",
    #                         arguments=result.model_dump_json(),
    #                     )
    #                 ],
    #                 source="assistant",
    #             )
    #         )
    #     else:
    #         user_message = UserMessage(content=message.content, source="user")
    #         # Add message to model context.
    #         await self._model_context.add_message(user_message)

    def weather_tool(self):
        def get_weather(city: str) -> str:
            return "sunny"

        return FunctionTool(get_weather, description="Get the weather of a city.")

    def social_login_tool(self):
        def social_login() -> str:
            json1 = SocialLoginInput(
                type="SocialLoginInput",
                username="username1",
                password="password1",
                otp_key="",
            ).model_dump_json()
            # self._model_context.add_message(
            #     AssistantMessage(
            #         content=[
            #             FunctionCall(
            #                 id=generate_uuid(),
            #                 name="social_login",
            #                 arguments=json1,
            #             )
            #         ],
            #         source="assistant",
            #     )
            # )
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
        self, message: ChatMessageInput, ctx: MessageContext
    ) -> None:
        """用户跟聊天助手的对话"""
        logger.info(f"handle_agent_run_input: {message}")
        await self._model_context.add_message(
            UserMessage(content=message.content, source="user")
        )

        assistant = AssistantAgent(
            "assistant",
            model_client=self.model_client,
            model_context=self._model_context,
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
        await self._model_context.add_message(
            AssistantMessage(
                content=response.chat_message.content,
                source=response.chat_message.source,
            )
        )

    @message_handler
    async def on_social_login(
        self, message: SocialLoginInput, ctx: MessageContext
    ) -> bool:
        login_result = self.ig_client.login(
            username=message.username,
            password=message.password,
            verification_code=pyotp.TOTP(message.otp_key).now(),
            relogin=False,
        )
        if not login_result:
            raise Exception("ig 登录失败")
        self._state.ig_settings = self.ig_client.get_settings()
        self._state.proxy_url = settings.default_proxy_url
        self._state.username = message.username
        self._state.password = message.password
        self._state.otp_key = message.otp_key
        return login_result

    async def save_state(self) -> Mapping[str, Any]:
        self._state.model_context = await self._model_context.save_state()
        return self._state.model_dump()

    async def load_state(self, state: Mapping[str, Any]) -> None:
        self._state = UserAgentState.from_dict(state)
        await self._model_context.load_state(self._state.model_context)
