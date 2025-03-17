from typing import Any

from autogen_agentchat.teams._group_chat._events import (
    GroupChatRequestPublish,
    GroupChatStart,
)
from autogen_core import (
    AgentId,
    DefaultInterventionHandler,
    DropMessage,
    MessageContext,
)
from loguru import logger
from mtmai.agents._types import GetSlowUserMessage


class NeedsUserInputHandler(DefaultInterventionHandler):
    def __init__(self):
        from mtmai.context.context_client import TenantClient

        self.question_for_user: GetSlowUserMessage | None = None
        self.tenant_client = TenantClient()

    async def on_publish(self, message: Any, *, message_context: MessageContext) -> Any:
        if isinstance(message, GetSlowUserMessage):
            logger.info(f"NeedsUserInputHandler(on_publish): {message.content}")
            self.question_for_user = message

        if isinstance(message, GroupChatStart):
            pass
        elif isinstance(message, GroupChatRequestPublish):
            pass
        else:
            await self.tenant_client.emit(message)
        return message

    async def on_send(
        self, message: Any, *, message_context: MessageContext, recipient: AgentId
    ) -> Any | type[DropMessage]:
        """Called when a message is submitted to the AgentRuntime using :meth:`autogen_core.base.AgentRuntime.send_message`."""
        logger.info(f"NeedsUserInputHandler.on_send: {message}")
        await self.tenant_client.emit(message)
        return message

    async def on_response(
        self, message: Any, *, sender: AgentId, recipient: AgentId | None
    ) -> Any | type[DropMessage]:
        """Called when a response is received by the AgentRuntime from an Agent's message handler returning a value."""
        logger.info(f"NeedsUserInputHandler.on_response: {message}")
        await self.tenant_client.emit(message)
        return message

    @property
    def needs_user_input(self) -> bool:
        return self.question_for_user is not None

    @property
    def user_input_content(self) -> str | None:
        if self.question_for_user is None:
            return None
        return self.question_for_user.content
