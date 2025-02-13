import logging
from typing import Awaitable, Callable, List
from autogen_core import  MessageContext, RoutedAgent, default_subscription, message_handler
from autogen_core.models import (
    AssistantMessage,
    ChatCompletionClient,
    LLMMessage,
    SystemMessage,
    UserMessage,
)
from mtmaisdk.clients.rest.models.chat_message import ChatMessage
from mtmaisdk.clients.rest.models.chat_message_create import ChatMessageCreate
from mtmaisdk.clients.rest_client import AsyncRestApi
from rich.console import Console
from rich.markdown import Markdown

logger = logging.getLogger(__name__)
@default_subscription
class UIAgent(RoutedAgent):
    """Handles UI-related tasks and message processing for the distributed group chat system."""

    def __init__(self, gomtmapi: AsyncRestApi) -> None:
        super().__init__("UI Agent")
        self.gomtmapi = gomtmapi

    @message_handler
    async def handle_message_chunk(self, message: ChatMessageCreate, ctx: MessageContext) -> None:
        logger.info(f"UI Agent 收到消息: {message}")

        await self.gomtmapi.chat_api.chat_create_message(
            tenant=message.tenant_id,
            chat_message_create=message,
            )
