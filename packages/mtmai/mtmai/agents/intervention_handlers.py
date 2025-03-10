from typing import Any
from venv import logger

from autogen_core import (
    AgentId,
    DefaultInterventionHandler,
    DropMessage,
    MessageContext,
)
from mtmai.agents._types import GetSlowUserMessage


class NeedsUserInputHandler(DefaultInterventionHandler):
    def __init__(self):
        self.question_for_user: GetSlowUserMessage | None = None

    async def on_publish(self, message: Any, *, message_context: MessageContext) -> Any:
        if isinstance(message, GetSlowUserMessage):
            logger.info(f"NeedsUserInputHandler: {message.content}")
            self.question_for_user = message
        return message

    async def on_send(
        self, message: Any, *, message_context: MessageContext, recipient: AgentId
    ) -> Any | type[DropMessage]:
        """Called when a message is submitted to the AgentRuntime using :meth:`autogen_core.base.AgentRuntime.send_message`."""
        logger.info(f"NeedsUserInputHandler.on_send: {message}")
        return message

    async def on_response(
        self, message: Any, *, sender: AgentId, recipient: AgentId | None
    ) -> Any | type[DropMessage]:
        """Called when a response is received by the AgentRuntime from an Agent's message handler returning a value."""
        logger.info(f"NeedsUserInputHandler.on_response: {message}")
        return message

    @property
    def needs_user_input(self) -> bool:
        return self.question_for_user is not None

    @property
    def user_input_content(self) -> str | None:
        if self.question_for_user is None:
            return None
        return self.question_for_user.content


# class TerminationHandler(DefaultInterventionHandler):
#     def __init__(self):
#         self.terminateMessage: TerminateMessage | None = None

#     async def on_publish(self, message: Any, *, message_context: MessageContext) -> Any:
#         if isinstance(message, TerminateMessage):
#             logger.info(f"Termination message received: {message.content}")
#             self.terminateMessage = message
#         return message

#     @property
#     def is_terminated(self) -> bool:
#         return self.terminateMessage is not None

#     @property
#     def termination_msg(self) -> str | None:
#         if self.terminateMessage is None:
#             return None
#         return self.terminateMessage.content
