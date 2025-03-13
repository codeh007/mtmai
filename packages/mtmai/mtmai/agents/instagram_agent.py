from ast import List
from typing import Any, Awaitable, Callable, Sequence

from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.base import Handoff as HandoffBase
from autogen_agentchat.base import Response
from autogen_agentchat.messages import ChatMessage
from autogen_core import CancellationToken, Component
from autogen_core.memory import Memory
from autogen_core.model_context import ChatCompletionContext
from autogen_core.models import ChatCompletionClient
from autogen_core.tools import BaseTool
from mtmai.clients.rest.models.instagram_agent_config import InstagramAgentConfig


class InstagramAgent(AssistantAgent, Component[InstagramAgentConfig]):
    component_config_schema = InstagramAgentConfig
    component_provider_override = "mtmai.agents.instagram_agent.InstagramAgent"

    def __init__(
        self,
        name: str,
        model_client: ChatCompletionClient,
        *,
        tools: List[
            BaseTool[Any, Any] | Callable[..., Any] | Callable[..., Awaitable[Any]]
        ]
        | None = None,
        handoffs: List[HandoffBase | str] | None = None,
        model_context: ChatCompletionContext | None = None,
        description: str = "An agent that provides assistance with ability to use tools.",
        system_message: (
            str | None
        ) = "You are a helpful AI assistant. Solve tasks using your tools. Reply with TERMINATE when the task has been completed.",
        model_client_stream: bool = False,
        reflect_on_tool_use: bool = False,
        tool_call_summary_format: str = "{result}",
        memory: Sequence[Memory] | None = None,
    ) -> None:
        super().__init__(
            name,
            model_client,
            tools,
            handoffs,
            model_context,
            description,
            system_message,
            model_client_stream,
            reflect_on_tool_use,
            tool_call_summary_format,
            memory,
        )

    # @message_handler
    # async def handle_user_task(self, message: UserTask, ctx: MessageContext) -> None:
    #     # human_input = input("Human agent input: ")
    #     human_input = await self.get_user_input("Human agent input: ")
    #     logger.info("TODO: need human input")
    #     logger.info(f"{'-'*80}\n{self.id.type}:\n{human_input}", flush=True)
    #     message.context.append(
    #         AssistantMessage(content=human_input, source=self.id.type)
    #     )
    #     await self.publish_message(
    #         AgentResponse(
    #             context=message.context, reply_to_topic_type=self._agent_topic_type
    #         ),
    #         topic_id=TopicId(self._user_topic_type, source=self.id.key),
    # )

    async def on_messages(
        self, messages: Sequence[ChatMessage], cancellation_token: CancellationToken
    ) -> Response:
        async for message in self.on_messages_stream(messages, cancellation_token):
            if isinstance(message, Response):
                return message
        raise AssertionError("The stream should have returned the final result.")
