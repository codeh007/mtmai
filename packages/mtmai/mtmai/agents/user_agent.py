from autogen_core import MessageContext, RoutedAgent, TopicId, message_handler
from autogen_core.models import UserMessage
from loguru import logger

from mtmai.agents._types import AgentResponse, UserLogin, UserTask


class UserAgent(RoutedAgent):
    def __init__(
        self, description: str, user_topic_type: str, agent_topic_type: str
    ) -> None:
        super().__init__(description)
        # self._user_topic_type = user_topic_type
        self._agent_topic_type = agent_topic_type

    @message_handler
    async def handle_user_login(self, message: UserLogin, ctx: MessageContext) -> None:
        logger.info(f"{'-'*80}\nUser login, session ID: {self.id.key}.", flush=True)
        # Get the user's initial input after login.
        user_input = input("User: ")
        logger.info(f"{'-'*80}\n{self.id.type}:\n{user_input}")
        await self.publish_message(
            UserTask(context=[UserMessage(content=user_input, source="User")]),
            topic_id=TopicId(self._agent_topic_type, source=self.id.key),
        )

    @message_handler
    async def handle_task_result(
        self, message: AgentResponse, ctx: MessageContext
    ) -> None:
        # Get the user's input after receiving a response from an agent.
        user_input = input("User (type 'exit' to close the session): ")
        logger.info(f"{'-'*80}\n{self.id.type}:\n{user_input}")
        if user_input.strip().lower() == "exit":
            logger.info(f"{'-'*80}\nUser session ended, session ID: {self.id.key}.")
            return
        message.context.append(UserMessage(content=user_input, source="User"))
        await self.publish_message(
            UserTask(context=message.context),
            topic_id=TopicId(message.reply_to_topic_type, source=self.id.key),
        )
