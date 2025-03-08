from autogen_core import MessageContext, RoutedAgent, message_handler
from loguru import logger

# from mtmai.agents._semantic_router_components import UserProxyMessage
from mtmai.agents._types import (
    AgentResponse,
    CodeReviewResult,
    CodeReviewTask,
    TerminationMessage,
)
from mtmai.clients.rest.models.chat_message_upsert import ChatMessageUpsert
from mtmai.context.context_client import TenantClient


class UserAgent(RoutedAgent):
    def __init__(
        self, description: str, user_topic_type: str, agent_topic_type: str
    ) -> None:
        super().__init__(description)
        self._agent_topic_type = agent_topic_type

    # @message_handler
    # async def handle_user_login(self, message: UserLogin, ctx: MessageContext) -> None:
    #     """可以理解为新对话的入口, 可以从数据库加载相关的上下文数据,包括用户信息,记忆,权限信息,等"""
    #     if ctx.cancellation_token.is_cancelled():
    #         return

    #     # session_id = ctx.topic_id.source
    #     session_id = self.id.key
    #     tenant_client = TenantClient()
    #     tid = tenant_client.tenant_id
    #     logger.info(
    #         f"{'-'*80}\nUser login, session ID: {session_id}. task: {message.content}"
    #     )
    #     user_input = message.content

    #     match user_input:
    #         case "/test_code":
    #             await self._runtime.publish_message(
    #                 message=CodeWritingTask(
    #                     task="Write a function to find the sum of all even numbers in a list."
    #                 ),
    #                 topic_id=TopicId(coder_agent_topic_type, source=session_id),
    #             )
    #             # CodeWritingTask(
    #             #         task="Write a function to find the sum of all even numbers in a list."
    #             #     )
    #         case "/test_open_browser":
    #             await self._runtime.publish_message(
    #                 message=BrowserOpenTask(url="https://playwright.dev/"),
    #                 topic_id=TopicId(browser_topic_type, source=session_id),
    #             )
    #         case "/test_browser_task":
    #             await self._runtime.publish_message(
    #                 message=BrowserTask(task="Open an online code editor programiz."),
    #                 topic_id=TopicId(browser_topic_type, source=session_id),
    #             )
    #         case "/test_team":
    #             await self._runtime.publish_message(
    #                 message=TeamRunnerTask(
    #                     task=user_input, team=team_runner_topic_type
    #                 ),
    #                 topic_id=TopicId(team_runner_topic_type, source=session_id),
    #             )
    #         # case _:
    #         #     await self._runtime.publish_message(
    #         #         message=UserLogin(task=user_input),
    #         #         topic_id=TopicId(user_topic_type, source=session_id),
    #         #     )

    #     # 加载对话历史
    #     message_history = await tenant_client.ag.chat_api.chat_messages_list(
    #         tenant=tid,
    #         chat=session_id,
    #     )

    #     await self.publish_message(
    #         UserTask(context=[UserMessage(content=user_input, source="User")]),
    #         topic_id=TopicId(self._agent_topic_type, source=session_id),
    #     )

    #     await tenant_client.ag.chat_api.chat_message_upsert(
    #         tenant=tid,
    #         chat_message_upsert=ChatMessageUpsert(
    #             tenant_id=tid,
    #             content=user_input,
    #             # component_id=self.id.key,
    #             thread_id=self.id.key,
    #             role="user",
    #             source="user",
    #         ),
    #     )

    # The User has sent a message that needs to be routed
    # @message_handler
    # async def route_to_agent(
    #     self, message: UserProxyMessage, ctx: MessageContext
    # ) -> None:
    #     assert ctx.topic_id is not None
    #     logger.debug(f"Received message from {message.source}: {message.content}")
    #     session_id = ctx.topic_id.source
    #     intent = await self._identify_intent(message)
    #     agent = await self._find_agent(intent)
    #     await self.contact_agent(agent, message, session_id)

    ## Use a lookup, search, or LLM to identify the most relevant agent for the intent
    # async def _find_agent(self, intent: str) -> str:
    #     logger.debug(f"Identified intent: {intent}")
    #     try:
    #         agent = await self._registry.get_agent(intent)
    #         return agent
    #     except KeyError:
    #         logger.debug("No relevant agent found for intent: " + intent)
    #         return "termination"

    # ## Forward user message to the appropriate agent, or end the thread.
    # async def contact_agent(
    #     self, agent: str, message: UserProxyMessage, session_id: str
    # ) -> None:
    #     if agent == "termination":
    #         logger.debug("No relevant agent found")
    #         await self.publish_message(
    #             TerminationMessage(
    #                 reason="No relevant agent found",
    #                 content=message.content,
    #                 source=self.type,
    #             ),
    #             DefaultTopicId(type="user_proxy", source=session_id),
    #         )
    #     else:
    #         logger.debug("Routing to agent: " + agent)
    #         await self.publish_message(
    #             UserProxyMessage(content=message.content, source=message.source),
    #             DefaultTopicId(type=agent, source=session_id),
    #         )

    # When a conversation ends
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
    async def handle_task_result(
        self, message: AgentResponse, ctx: MessageContext
    ) -> None:
        tenant_client = TenantClient()
        tid = tenant_client.tenant_id
        llm_message = message.context[-1]
        await tenant_client.emit(llm_message)
        await tenant_client.ag.chat_api.chat_message_upsert(
            tenant=tid,
            chat_message_upsert=ChatMessageUpsert(
                tenant_id=tid,
                content=llm_message.content,
                # component_id=self.id.key,
                thread_id=self.id.key,
                role="assistant",
                source="assistant",
            ),
        )

        # await tenant_client.emit(message)
        # user_input = await self.get_user_input(
        #     "User (type 'exit' to close the session): ",
        #     ctx,
        # )
        # logger.info(f"{'-'*80}\n{self.id.type}:\n{user_input}")

        # if user_input.strip().lower() == "exit":
        #     logger.info(f"{'-'*80}\nUser session ended, session ID: {self.id.key}.")
        #     return
        # message.context.append(UserMessage(content=user_input, source="User"))
        # await self.publish_message(
        #     UserTask(context=message.context),
        #     topic_id=TopicId(message.reply_to_topic_type, source=self.id.key),
        # )

    # async def get_user_input(self, prompt: str, ctx: MessageContext) -> str:
    #     """Get user input from the console. Override this method to customize how user input is retrieved."""
    #     logger.info(f"TODO: need user input, ctx: {ctx}")
    #     user_input = "TODO: need user input"
    #     # loop = asyncio.get_event_loop()
    #     # return await loop.run_in_executor(None, input, prompt)
    #     return user_input

    @message_handler
    async def handle_code_review_task(
        self, message: CodeReviewTask, ctx: MessageContext
    ) -> None:
        logger.info(f"handle_user_message: {message}")
        tenant_client = TenantClient()
        await tenant_client.emit(message)

    async def handle_code_review_result(
        self, message: CodeReviewResult, ctx: MessageContext
    ) -> None:
        logger.info(f"handle_code_review_result: {message}")
        tenant_client = TenantClient()
        await tenant_client.emit(message)
