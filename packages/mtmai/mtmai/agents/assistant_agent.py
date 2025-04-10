from textwrap import dedent
from typing import Any, Awaitable, Callable, List, Optional

from autogen_agentchat.agents import AssistantAgent as AutogenAssistantAgent
from autogen_core import Component
from autogen_core.tools import BaseTool
from mtmai.clients.rest.models.assistant_agent_config import AssistantAgentConfig
from mtmai.model_client.model_client import MtOpenAIChatCompletionClient
from pydantic import BaseModel


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
        model_client: MtOpenAIChatCompletionClient,
        *,
        tools: List[
            BaseTool[BaseModel, BaseModel]
            | Callable[..., Any]
            | Callable[..., Awaitable[Any]]
        ]
        | None = None,
        description: Optional[str] = None,
        system_message: Optional[str] = None,
    ):
        super().__init__(
            name=name,
            model_client=model_client,
            tools=tools
            or [
                # get_video_length,
                # get_screenshot_at,
                # save_screenshot,
                # self.vs_transribe_video_screenshot,
                # extract_audio,
                # transcribe_audio_with_timestamps,
            ],
            description=description or self.DEFAULT_DESCRIPTION,
            system_message=system_message or self.DEFAULT_SYSTEM_MESSAGE,
        )
