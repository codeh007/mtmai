from textwrap import dedent
from typing import Any, Awaitable, Callable, Dict, List, Sequence

from autogen_agentchat.agents import AssistantAgent as AutogenAssistantAgent
from autogen_agentchat.base import Handoff as HandoffBase
from autogen_core import Component
from autogen_core.memory import Memory
from autogen_core.model_context import ChatCompletionContext
from autogen_core.models import ChatCompletionClient
from autogen_core.tools import BaseTool
from mtmai.clients.rest.models.assistant_agent_config import AssistantAgentConfig
from mtmai.model_client.model_client import MtOpenAIChatCompletionClient
from mtmai.mtlibs.autogen_utils.component_loader import ComponentLoader
from pydantic import BaseModel
from typing_extensions import Self


class AssistantAgent(AutogenAssistantAgent, Component[AssistantAgentConfig]):
    component_provider_override = "mtmai.agents.assistant_agent.AssistantAgent"
    component_config_schema = AssistantAgentConfig

    DEFAULT_DESCRIPTION = "An agent that provides assistance with ability to use tools."

    DEFAULT_SYSTEM_MESSAGE = dedent("""
    You are a helpful AI assistant. Solve tasks using your tools. Reply with TERMINATE when the task has been completed.
    """)

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
        reflect_on_tool_use: bool | None = None,
        tool_call_summary_format: str = "{result}",
        output_content_type: type[BaseModel] | None = None,
        memory: Sequence[Memory] | None = None,
        metadata: Dict[str, str] | None = None,
    ):
        super().__init__(
            name=name,
            model_client=model_client,
            tools=tools or [],
            handoffs=handoffs,
            model_context=model_context,
            description=description or self.DEFAULT_DESCRIPTION,
            system_message=system_message or self.DEFAULT_SYSTEM_MESSAGE,
            model_client_stream=model_client_stream,
            reflect_on_tool_use=reflect_on_tool_use,
            tool_call_summary_format=tool_call_summary_format,
            output_content_type=output_content_type,
            memory=memory,
            metadata=metadata,
        )

    def _to_config(self) -> AssistantAgentConfig:
        """Convert the assistant agent to a declarative config."""

        if self._output_content_type:
            raise ValueError(
                "AssistantAgent with output_content_type does not support declarative config."
            )

        return AssistantAgentConfig(
            name=self.name,
            model_client=self._model_client.dump_component(),
            tools=[tool.dump_component() for tool in self._tools],
            handoffs=list(self._handoffs.values()) if self._handoffs else None,
            model_context=self._model_context.dump_component(),
            memory=[memory.dump_component() for memory in self._memory]
            if self._memory
            else None,
            description=self.description,
            system_message=self._system_messages[0].content
            if self._system_messages
            and isinstance(self._system_messages[0].content, str)
            else None,
            model_client_stream=self._model_client_stream,
            reflect_on_tool_use=self._reflect_on_tool_use,
            tool_call_summary_format=self._tool_call_summary_format,
            metadata=self._metadata,
        )

    @classmethod
    def _from_config(cls, config: AssistantAgentConfig) -> Self:
        return cls(
            name=config.name,
            model_client=ComponentLoader.load_component(
                config.model_client, expected=MtOpenAIChatCompletionClient
            ),
            tools=[
                ComponentLoader.load_component(tool, expected=BaseTool)
                for tool in config.tools
            ]
            if config.tools
            else None,
            handoffs=config.handoffs,
            model_context=None,
            memory=[
                ComponentLoader.load_component(memory, expected=Memory)
                for memory in config.memory
            ]
            if config.memory
            else None,
            description=config.description,
            system_message=config.system_message,
            model_client_stream=config.model_client_stream,
            reflect_on_tool_use=config.reflect_on_tool_use,
            tool_call_summary_format=config.tool_call_summary_format,
            metadata=config.metadata,
        )
