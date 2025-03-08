from autogen_core import MessageContext, RoutedAgent, message_handler
from loguru import logger
from mtmai.agents._types import PlatformAccountTask


class PlatformAccountAgent(RoutedAgent):
    def __init__(
        self,
        description: str,
        # system_message: SystemMessage,
        # model_client: ChatCompletionClient,
        # tools: List[Tool],
        # delegate_tools: List[Tool],
        # agent_topic_type: str,
        # user_topic_type: str,
    ) -> None:
        super().__init__(description)
        # self._system_message = system_message
        # self._model_client = model_client
        # self._tools = dict([(tool.name, tool) for tool in tools])
        # self._tool_schema = [tool.schema for tool in tools]
        # self._delegate_tools = dict([(tool.name, tool) for tool in delegate_tools])
        # self._delegate_tool_schema = [tool.schema for tool in delegate_tools]
        # self._agent_topic_type = agent_topic_type
        # self._user_topic_type = user_topic_type

    @message_handler
    async def handle_task(
        self, message: PlatformAccountTask, ctx: MessageContext
    ) -> None:
        logger.info(f"Platform account agent received task: {message}")
