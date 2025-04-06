from typing import Any, Mapping

from autogen_core import (
    AgentId,
    FunctionCall,
    MessageContext,
    RoutedAgent,
    TopicId,
    message_handler,
)
from autogen_core.model_context import BufferedChatCompletionContext
from autogen_core.models import AssistantMessage, SystemMessage, UserMessage
from loguru import logger
from mtmai.agents._types import (
    BrowserOpenTask,
    BrowserTask,
    CodeWritingTask,
    IgLoginRequire,
    TerminationMessage,
)
from mtmai.clients.rest.models.agent_topic_types import AgentTopicTypes
from mtmai.clients.rest.models.agent_user_input import AgentUserInput
from mtmai.clients.rest.models.social_add_followers_input import SocialAddFollowersInput
from mtmai.mtlibs.id import generate_uuid


class UserAgent(RoutedAgent):
    def __init__(
        self, description: str, session_id: str, social_agent_topic_type: str = None
    ) -> None:
        super().__init__(description)
        self._social_agent_topic_type = social_agent_topic_type
        self._model_context = BufferedChatCompletionContext(buffer_size=10)
        self._session_id = session_id
        self.instagram_agent_id = AgentId(self._social_agent_topic_type, "default")

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
                # IgAccountMessage(username="username1", password="password1"), agent_id
                SocialAddFollowersInput(
                    username="username1",
                    password="password1",
                    target_username="target_username1",
                ),
                agent_id,
            )
            # logger.info(f"result: {result}")
            if isinstance(result, IgLoginRequire):
                self.is_waiting_ig_login = True
            await self._model_context.add_message(
                SystemMessage(
                    content="hello system message",
                )
            )
            await self._model_context.add_message(
                UserMessage(
                    content="hello user message",
                    source="user",
                )
            )
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

    # @message_handler
    # async def handle_social_add_followers_input(
    #     self, message: SocialAddFollowersInput, ctx: MessageContext
    # ) -> None:
    #     logger.info(f"handle_social_add_followers_input: {message}")
    #     await self._model_context.add_message(
    #         UserMessage(content=message.model_dump_json(), source="user")
    #     )
    #     result = await self._runtime.send_message(
    #         message,
    #         self.instagram_agent_id,
    #     )
    #     return result

    # @message_handler
    # async def on_ig_login(self, message: SocialLoginInput, ctx: MessageContext) -> None:
    #     result = await self._runtime.send_message(
    #         message,
    #         agent_id=AgentId(self._social_agent_topic_type, "default"),
    #     )
    #     return result

    @message_handler
    async def on_terminate(
        self, message: TerminationMessage, ctx: MessageContext
    ) -> None:
        assert ctx.topic_id is not None
        logger.info(f"对话结束 with {ctx.sender} because {message.reason}")

    async def save_state(self) -> Mapping[str, Any]:
        return {
            "model_context": await self._model_context.save_state(),
            # "is_waiting_ig_login": self.is_waiting_ig_login,
        }

    async def load_state(self, state: Mapping[str, Any]) -> None:
        self._model_context.load_state(state["model_context"])
        self.is_waiting_ig_login = state.get("is_waiting_ig_login", False)
