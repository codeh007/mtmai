from typing import AsyncGenerator, Union

from google.adk.agents import BaseAgent
from google.adk.agents.invocation_context import InvocationContext
from google.adk.events import Event
from google.adk.models import BaseLlm
from google.genai import types  # noqa: F401
from smolagents import CodeAgent
from typing_extensions import override

from mtmai.model_client.utils import get_default_smolagents_model
from mtmai.mtlibs.adk_utils.run_utils import adk_run_smolagent


class AdkSmolAgent(BaseAgent):
    """
    用 adk agent 封装 smolagent 的 CodeAgent

    """

    model_config = {"arbitrary_types_allowed": True}
    max_steps: int = 20
    verbosity_level: int = 2
    additional_authorized_imports: list[str] = ["*"]
    model: Union[str, BaseLlm] | None = None

    def __init__(
        self,
        name: str,
        description: str = "擅长使用 python 编程解决复杂任务",
        max_steps: int = 20,
        verbosity_level: int = 2,
        additional_authorized_imports: list[str] = ["*"],
        model: Union[str, BaseLlm] | None = None,
    ):
        super().__init__(
            name=name,
            description=description,
            max_steps=max_steps,
            verbosity_level=verbosity_level,
            additional_authorized_imports=additional_authorized_imports,
            model=model,
        )

    @override
    async def _run_async_impl(
        self, ctx: InvocationContext
    ) -> AsyncGenerator[Event, None]:
        agent = CodeAgent(
            tools=[],
            model=self.model or get_default_smolagents_model(),
            additional_authorized_imports=self.additional_authorized_imports,
            max_steps=self.max_steps,
            verbosity_level=self.verbosity_level,
        )
        async for event in adk_run_smolagent(agent=agent, ctx=ctx):
            yield event
