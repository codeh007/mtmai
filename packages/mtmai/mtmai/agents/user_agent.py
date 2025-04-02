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
    AgentResponse,
    BrowserOpenTask,
    BrowserTask,
    CodeWritingTask,
    IgAccountMessage,
    IgLoginRequire,
    TerminationMessage,
)
from mtmai.clients.rest.models.agent_run_input import AgentRunInput
from mtmai.clients.rest.models.agent_topic_types import AgentTopicTypes
from mtmai.mtlibs.id import generate_uuid


class UserAgent(RoutedAgent):
    def __init__(self, description: str, agent_topic_type: str = None) -> None:
        super().__init__(description)
        self._agent_topic_type = agent_topic_type
        self._model_context = BufferedChatCompletionContext(buffer_size=7)
        self.username = None
        self.password = None
        self.is_waiting_ig_login = False

    @message_handler
    async def handle_agent_run_input(
        self, message: AgentRunInput, ctx: MessageContext
    ) -> IgLoginRequire | None:
        """可以理解为新对话的入口, 可以从数据库加载相关的上下文数据,包括用户信息,记忆,权限信息,等"""
        if ctx.cancellation_token.is_cancelled():
            return

        session_id = self.id.key
        # tenant_client = TenantClient()
        # tid = tenant_client.tenant_id
        logger.info(
            f"{'-'*80}\nhandle_agent_run_input, session ID: {session_id}. task: {message.content}"
        )
        user_content = message.content
        if user_content.startswith("/test_code"):
            await self.runtime.publish_message(
                message=CodeWritingTask(
                    task="Write a function to find the sum of all even numbers in a list."
                ),
                topic_id=TopicId(AgentTopicTypes.CODER, source=session_id),
            )
        elif user_content.startswith("/test_open_browser"):
            await self.runtime.publish_message(
                message=BrowserOpenTask(url="https://playwright.dev/"),
                topic_id=TopicId(AgentTopicTypes.BROWSER, source=session_id),
            )
        elif user_content.startswith("/test_browser_task"):
            await self.runtime.publish_message(
                message=BrowserTask(task="Open an online code editor programiz."),
                topic_id=TopicId(AgentTopicTypes.BROWSER, source=session_id),
            )
        # elif user_content.startswith("/test_team"):
        #     await self.runtime.publish_message(
        #         message=TeamRunnerTask(task=user_content, team=team_runner_topic_type),
        #         topic_id=TopicId(team_runner_topic_type, source=session_id),
        #     )
        elif user_content.startswith("/test_ig_login"):
            # await self.runtime.publish_message(
            #     message=IgAccountMessage(username="username1", password="password1"),
            #     topic_id=TopicId(instagram_agent_topic_type, source=session_id),
            # )
            agent_id = AgentId(AgentTopicTypes.INSTAGRAM, "default")
            result = await self._runtime.send_message(
                IgAccountMessage(username="username1", password="password1"), agent_id
            )
            logger.info(f"result: {result}")
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

    @message_handler
    async def on_terminate(
        self, message: TerminationMessage, ctx: MessageContext
    ) -> None:
        assert ctx.topic_id is not None
        logger.info(f"对话结束 with {ctx.sender} because {message.reason}")
        # await self.publish_message(
        #     FinalResult(content=message.content, source=self.id.key),
        #     topic_id=DefaultTopicId(type="response", source=ctx.topic_id.source),
        # )

    @message_handler
    async def on_ig_login(self, message: IgLoginRequire, ctx: MessageContext) -> None:
        # assert ctx.topic_id is not None
        logger.info(f"on_ig_login with {ctx.sender} because {message.reason}")

    @message_handler
    async def handle_task_result(
        self, message: AgentResponse, ctx: MessageContext
    ) -> None:
        # tenant_client = TenantClient()
        # tid = tenant_client.tenant_id
        # llm_message = message.context[-1]
        # await tenant_client.emit(llm_message)
        # await tenant_client.ag.chat_api.chat_message_upsert(
        #     tenant=tid,
        #     chat_message_upsert=ChatMessageUpsert(
        #         tenant_id=tid,
        #         content=llm_message.content,
        #         # component_id=self.id.key,
        #         thread_id=self.id.key,
        #         role="assistant",
        #         # source="assistant",
        #         source=ctx.topic_id.source,
        #         topic=ctx.topic_id.type,
        #     ),
        # )
        pass

    async def save_state(self) -> Mapping[str, Any]:
        return {
            "model_context": await self._model_context.save_state(),
            "is_waiting_ig_login": self.is_waiting_ig_login,
        }

    async def load_state(self, state: Mapping[str, Any]) -> None:
        self._model_context.load_state(state["model_context"])
        self.is_waiting_ig_login = state.get("is_waiting_ig_login", False)
