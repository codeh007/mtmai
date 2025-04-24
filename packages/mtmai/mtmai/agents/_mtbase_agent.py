from typing import AsyncGenerator

from google.adk.agents import BaseAgent
from google.adk.agents.invocation_context import InvocationContext
from google.adk.events import Event
from google.genai import types  # noqa: F401
from typing_extensions import override


class MtBaseAgent(BaseAgent):
    """
    base agent
    """

    model_config = {"arbitrary_types_allowed": True}

    def __init__(
        self,
        name: str,
        description: str = "base agent",
    ):
        super().__init__(
            name=name,
            description=description,
        )

    @override
    async def _run_async_impl(
        self, ctx: InvocationContext
    ) -> AsyncGenerator[Event, None]:
        for event in super()._run_async_impl(ctx):
            yield event
