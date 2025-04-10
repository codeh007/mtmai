from typing import Any

from autogen_agentchat.teams._group_chat._events import (
    GroupChatRequestPublish,
    GroupChatStart,
)
from autogen_core import (
    AgentId,
    DefaultInterventionHandler,
    DropMessage,
    FunctionCall,
    MessageContext,
)
from autogen_core.tool_agent import ToolException
from loguru import logger
from mtlibs.autogen_utils._types import GetSlowUserMessage


class NeedsUserInputHandler(DefaultInterventionHandler):
    def __init__(self, session_id: str):
        from mtmai.clients.tenant_client import TenantClient

        self.question_for_user: GetSlowUserMessage | None = None
        self.tenant_client = TenantClient()
        self.session_id = session_id

    async def on_publish(self, message: Any, *, message_context: MessageContext) -> Any:
        if isinstance(message, GetSlowUserMessage):
            logger.info(f"InputHandler(on_publish): {message.content}")
            self.question_for_user = message
        return message

    async def on_send(
        self, message: Any, *, message_context: MessageContext, recipient: AgentId
    ) -> Any | type[DropMessage]:
        """Called when a message is submitted to the AgentRuntime using :meth:`autogen_core.base.AgentRuntime.send_message`."""
        logger.info(
            f"InputHandler.on_send: {message}\n  recipient: {recipient}\nmessage_context: {message_context}"
        )
        await self.emit_message_event(message)
        return message

    # async def on_response(
    #     self, message: Any, *, sender: AgentId, recipient: AgentId | None
    # ) -> Any | type[DropMessage]:
    #     """Called when a response is received by the AgentRuntime from an Agent's message handler returning a value."""
    #     logger.info(f"intervention(on_response): {message}")
    #     await self.emit_message_event(message)
    #     return message

    @property
    def needs_user_input(self) -> bool:
        return self.question_for_user is not None

    @property
    def user_input_content(self) -> str | None:
        if self.question_for_user is None:
            return None
        return self.question_for_user.content

    async def emit_message_event(self, message: Any):
        if not message:
            return
        if isinstance(message, GroupChatStart):
            pass
        elif isinstance(message, GroupChatRequestPublish):
            pass
        else:
            await self.tenant_client.emit(message)


class ToolInterventionHandler(DefaultInterventionHandler):
    async def on_send(
        self, message: Any, *, message_context: MessageContext, recipient: AgentId
    ) -> Any | type[DropMessage]:
        if isinstance(message, FunctionCall):
            # Request user prompt for tool execution.
            user_input = input(
                f"Function call: {message.name}\nArguments: {message.arguments}\nDo you want to execute the tool? (y/n): "
            )
            if user_input.strip().lower() != "y":
                raise ToolException(
                    content="User denied tool execution.",
                    call_id=message.id,
                    name=message.name,
                )
        return message
