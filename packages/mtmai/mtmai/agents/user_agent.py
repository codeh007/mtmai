from typing import Any, Mapping

from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.messages import TextMessage
from autogen_core import (
    AgentId,
    FunctionCall,
    MessageContext,
    RoutedAgent,
    TopicId,
    message_handler,
)
from autogen_core.model_context import BufferedChatCompletionContext
from autogen_core.models import AssistantMessage, ChatCompletionClient, UserMessage
from autogen_core.tools import Tool
from autogen_ext.code_executors.docker import DockerCommandLineCodeExecutor
from autogen_ext.tools.code_execution import PythonCodeExecutionTool
from loguru import logger
from mtmai.agents._types import (
    BrowserOpenTask,
    BrowserTask,
    CodeWritingTask,
    IgLoginRequire,
)
from mtmai.clients.rest.models.agent_topic_types import AgentTopicTypes
from mtmai.clients.rest.models.agent_user_input import AgentUserInput
from mtmai.clients.rest.models.chat_message_input import ChatMessageInput
from mtmai.clients.rest.models.social_add_followers_input import SocialAddFollowersInput
from mtmai.clients.rest.models.user_agent_state import UserAgentState
from mtmai.mtlibs.id import generate_uuid


class UserAgent(RoutedAgent):
    def __init__(
        self,
        description: str,
        session_id: str,
        model_client: ChatCompletionClient | None = None,
        social_agent_topic_type: str = None,
    ) -> None:
        super().__init__(description)
        self._social_agent_topic_type = social_agent_topic_type
        self._model_context = BufferedChatCompletionContext(buffer_size=15)
        self._session_id = session_id
        self.model_client = model_client
        self.instagram_agent_id = AgentId(self._social_agent_topic_type, "default")

        self._state = UserAgentState()

    @message_handler
    async def handle_agent_run_input(
        self, message: AgentUserInput, ctx: MessageContext
    ) -> None:
        """用户输入"""
        if ctx.cancellation_token.is_cancelled():
            return

        session_id = self.id.key
        logger.info(
            f"{'-'*80}\nhandle_agent_run_input, session ID: {session_id}. task: {message.content}"
        )
        user_content = message.content
        if user_content.startswith("/test_code"):
            await self.runtime.publish_message(
                message=CodeWritingTask(
                    task="Write a function to find the sum of all even numbers in a list."
                ),
                topic_id=TopicId(AgentTopicTypes.CODER.value, source=session_id),
            )
        elif user_content.startswith("/test_open_browser"):
            await self.runtime.publish_message(
                message=BrowserOpenTask(url="https://playwright.dev/"),
                topic_id=TopicId(AgentTopicTypes.BROWSER.value, source=session_id),
            )
        elif user_content.startswith("/test_browser_task"):
            await self.runtime.publish_message(
                message=BrowserTask(task="Open an online code editor programiz."),
                topic_id=TopicId(AgentTopicTypes.BROWSER.value, source=session_id),
            )
        elif user_content.startswith("/test/ig"):
            agent_id = AgentId(self._social_agent_topic_type, "default")
            result = await self._runtime.send_message(
                SocialAddFollowersInput(
                    username="username1",
                    password="password1",
                    target_username="target_username1",
                ),
                agent_id,
            )
            if isinstance(result, IgLoginRequire):
                self.is_waiting_ig_login = True

            await self._model_context.add_message(
                AssistantMessage(
                    content=[
                        FunctionCall(
                            id=generate_uuid(),
                            name="ig_login",
                            arguments=result.model_dump_json(),
                        )
                    ],
                    source="assistant",
                )
            )
        else:
            user_message = UserMessage(content=message.content, source="user")
            # Add message to model context.
            await self._model_context.add_message(user_message)

    async def get_tools(self, ctx: MessageContext) -> list[Tool]:
        # Create the tool.
        code_executor = DockerCommandLineCodeExecutor()
        await code_executor.start()
        code_execution_tool = PythonCodeExecutionTool(code_executor)
        # Use the tool directly without an agent.
        # code = "print('Hello, world!')"
        # result = await code_execution_tool.run_json({"code": code}, ctx.cancellation_token)
        return [code_execution_tool]

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
            system_message="你是实用助手,需要使用提供的工具解决用户提出的问题",
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

    async def save_state(self) -> Mapping[str, Any]:
        self._state.model_context = await self._model_context.save_state()
        return self._state.model_dump()

    async def load_state(self, state: Mapping[str, Any]) -> None:
        self._state = UserAgentState.from_dict(state)
        await self._model_context.load_state(self._state.model_context)
