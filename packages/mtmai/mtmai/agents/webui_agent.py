from typing import Awaitable, Callable, List
from uuid import uuid4
from dataclasses import dataclass
from autogen_core import DefaultTopicId, MessageContext, RoutedAgent, message_handler
from autogen_core.models import (
    AssistantMessage,
    ChatCompletionClient,
    LLMMessage,
    SystemMessage,
    UserMessage,
)
from autogen_ext.runtimes.grpc import GrpcWorkerAgentRuntime
from rich.console import Console
from rich.markdown import Markdown

from ._types import MessageChunk



class UIAgent(RoutedAgent):
    """Handles UI-related tasks and message processing for the distributed group chat system."""

    def __init__(self, on_message_chunk_func: Callable[[MessageChunk], Awaitable[None]]) -> None:
        super().__init__("UI Agent")
        self._on_message_chunk_func = on_message_chunk_func

    @message_handler
    async def handle_message_chunk(self, message: MessageChunk, ctx: MessageContext) -> None:
        await self._on_message_chunk_func(message)