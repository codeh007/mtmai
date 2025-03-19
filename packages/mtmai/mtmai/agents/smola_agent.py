from typing import Any, Awaitable, Callable, List, Sequence

from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.base import Handoff as HandoffBase
from autogen_agentchat.base import Response
from autogen_agentchat.messages import ChatMessage
from autogen_core import CancellationToken, Component
from autogen_core.memory import Memory
from autogen_core.model_context import ChatCompletionContext
from autogen_core.models import ChatCompletionClient
from autogen_core.tools import BaseTool
from loguru import logger
from mtmai.clients.rest.models.smola_agent_config import SmolaAgentConfig
from typing_extensions import Self


class SmolaAgent(AssistantAgent, Component[SmolaAgentConfig]):
    component_config_schema = SmolaAgentConfig
    component_provider_override = "mtmai.agents.smola_agent.SmolaAgent"

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
            name=name,
            model_client=model_client,
            tools=tools,
            handoffs=handoffs,
            model_context=model_context,
            description=description,
            system_message=system_message,
            model_client_stream=model_client_stream,
            reflect_on_tool_use=reflect_on_tool_use,
            tool_call_summary_format=tool_call_summary_format,
            memory=memory,
        )

    async def on_messages(
        self, messages: Sequence[ChatMessage], cancellation_token: CancellationToken
    ) -> Response:
        from smolagents import CodeAgent, DuckDuckGoSearchTool, HfApiModel

        model = HfApiModel()
        agent = CodeAgent(tools=[DuckDuckGoSearchTool()], model=model)

        result = agent.run(
            "How many seconds would it take for a leopard at full speed to run through Pont des Arts?"
        )
        logger.info(f"result: {result}")

    @classmethod
    def _from_config(cls, config: SmolaAgentConfig) -> Self:
        """Create an assistant agent from a declarative config."""

        # _config = config
        return cls(
            name=config.name,
            model_client=ChatCompletionClient.load_component(
                config.model_client.model_dump()
            ),
            tools=[BaseTool.load_component(tool) for tool in config.tools]
            if config.tools
            else None,
            handoffs=config.handoffs,
            model_context=None,
            memory=[Memory.load_component(memory) for memory in config.memory]
            if config.memory
            else None,
            description=config.description,
            system_message=config.system_message,
            model_client_stream=config.model_client_stream,
            reflect_on_tool_use=config.reflect_on_tool_use,
            tool_call_summary_format=config.tool_call_summary_format,
        )
