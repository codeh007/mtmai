from autogen_core import MessageContext, RoutedAgent, TopicId, message_handler
from autogen_core.models import AssistantMessage
from loguru import logger

from mtmai.agents._types import AgentResponse, UserTask


class HumanAgent(RoutedAgent):
    def __init__(
        self, description: str, agent_topic_type: str, user_topic_type: str
    ) -> None:
        super().__init__(description)
        self._agent_topic_type = agent_topic_type
        self._user_topic_type = user_topic_type

    @message_handler
    async def handle_user_task(self, message: UserTask, ctx: MessageContext) -> None:
        # human_input = input("Human agent input: ")
        human_input = await self.get_user_input("Human agent input: ")
        logger.info("TODO: need human input")
        logger.info(f"{'-'*80}\n{self.id.type}:\n{human_input}", flush=True)
        message.context.append(
            AssistantMessage(content=human_input, source=self.id.type)
        )
        await self.publish_message(
            AgentResponse(
                context=message.context, reply_to_topic_type=self._agent_topic_type
            ),
            topic_id=TopicId(self._user_topic_type, source=self.id.key),
        )

    async def get_user_input(self, prompt: str) -> str:
        """Get user input from the console. Override this method to customize how user input is retrieved."""
        # loop = asyncio.get_event_loop()
        # return await loop.run_in_executor(None, input, prompt)
        return "TODO: need human input"
