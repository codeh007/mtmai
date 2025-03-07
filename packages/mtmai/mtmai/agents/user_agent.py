from autogen_core import MessageContext, RoutedAgent, TopicId, message_handler
from autogen_core.models import UserMessage
from loguru import logger

from mtmai.agents._types import AgentResponse, TerminationMessage, UserLogin, UserTask
from mtmai.clients.rest.models.chat_message_upsert import ChatMessageUpsert
from mtmai.context.context_client import TenantClient


class UserAgent(RoutedAgent):
    def __init__(
        self, description: str, user_topic_type: str, agent_topic_type: str
    ) -> None:
        super().__init__(description)
        self._agent_topic_type = agent_topic_type

    @message_handler
    async def handle_user_login(self, message: UserLogin, ctx: MessageContext) -> None:
        """可以理解为新对话的入口, 可以从数据库加载相关的上下文数据,包括用户信息,记忆,权限信息,等"""
        if ctx.cancellation_token.is_cancelled():
            return

        # session_id = get_chat_session_id_ctx()
        # session_id = ctx.topic_id.source
        session_id = self.id.key
        tenant_client = TenantClient()
        tid = tenant_client.tenant_id
        logger.info(
            f"{'-'*80}\nUser login, session ID: {session_id}. task: {message.task}"
        )
        user_input = message.task
        await self.publish_message(
            UserTask(context=[UserMessage(content=user_input, source="User")]),
            topic_id=TopicId(self._agent_topic_type, source=session_id),
        )

        await tenant_client.ag.chat_api.chat_message_upsert(
            tenant=tid,
            chat_message_upsert=ChatMessageUpsert(
                tenant_id=tid,
                content=user_input,
                # component_id=self.id.key,
                thread_id=self.id.key,
                role="user",
                source="user",
            ),
        )

        # 似乎不需要
        # await tenant_client.emit(
        #     ChatSessionStartEvent(
        #         threadId=session_id,
        #     )
        # )

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
