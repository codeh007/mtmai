from typing import List

from autogen_agentchat.messages import TextMessage
from autogen_core import (
    AgentId,
    AgentType,
    MessageContext,
    RoutedAgent,
    message_handler,
)
from autogen_core.models import (
    ChatCompletionClient,
    LLMMessage,
    SystemMessage,
    UserMessage,
)
from autogen_core.tool_agent import tool_agent_caller_loop
from autogen_core.tools import ToolSchema
from mtmai.clients.rest.models.chat_message_input import ChatMessageInput


class ToolUseAgent(RoutedAgent):
    """An agent that uses tools to perform tasks. It executes the tools
    by itself by sending the tool execution task to a ToolAgent."""

    def __init__(
        self,
        description: str,
        system_messages: List[SystemMessage],
        model_client: ChatCompletionClient,
        tool_schema: List[ToolSchema],
        tool_agent_type: AgentType,
    ) -> None:
        super().__init__(description)
        self._model_client = model_client
        self._system_messages = system_messages
        self._tool_schema = tool_schema
        self._tool_agent_id = AgentId(type=tool_agent_type, key=self.id.key)

    @message_handler
    async def handle_user_message(
        self, message: ChatMessageInput, ctx: MessageContext
    ) -> TextMessage:
        """Handle a user message, execute the model and tools, and returns the response."""
        session: List[LLMMessage] = [
            UserMessage(content=message.content, source="User")
        ]
        # Use the tool agent to execute the tools, and get the output messages.
        output_messages = await tool_agent_caller_loop(
            self,
            tool_agent_id=self._tool_agent_id,
            model_client=self._model_client,
            input_messages=session,
            tool_schema=self._tool_schema,
            cancellation_token=ctx.cancellation_token,
        )
        # Extract the final response from the output messages.
        final_response = output_messages[-1].content
        assert isinstance(final_response, str)
        return TextMessage(content=final_response)
