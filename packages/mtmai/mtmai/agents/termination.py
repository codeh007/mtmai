from typing import Sequence

from autogen_agentchat.base import TerminatedException, TerminationCondition
from autogen_agentchat.messages import (
    AgentEvent,
    ChatMessage,
    StopMessage,
    ToolCallExecutionEvent,
)
from autogen_core import Component
from loguru import logger
from mtmai.context.ctx import get_step_canceled_ctx
from pydantic import BaseModel
from typing_extensions import Self


class MyFunctionCallTerminationConfig(BaseModel):
    """Configuration for the termination condition to allow for serialization
    and deserialization of the component.
    """

    function_name: str


class MyFunctionCallTermination(
    TerminationCondition, Component[MyFunctionCallTerminationConfig]
):
    """Terminate the conversation if a FunctionExecutionResult with a specific name is received."""

    component_config_schema = MyFunctionCallTerminationConfig
    """The schema for the component configuration."""

    def __init__(self, function_name: str) -> None:
        self._terminated = False
        self._function_name = function_name

    @property
    def terminated(self) -> bool:
        return self._terminated

    async def __call__(
        self, messages: Sequence[AgentEvent | ChatMessage]
    ) -> StopMessage | None:
        if self._terminated:
            raise TerminatedException("Termination condition has already been reached")

        step_canceled = get_step_canceled_ctx()
        if step_canceled:
            logger.info(
                "=========================Step canceled========================="
            )
            return StopMessage(
                content="Step canceled",
                source="MyFunctionCallTermination",
            )
        for message in messages:
            logger.info(f"(MyFunctionCallTermination)\nmessages: {messages}\n")
            if isinstance(message, ToolCallExecutionEvent):
                for execution in message.content:
                    if execution.name == self._function_name:
                        self._terminated = True
                        return StopMessage(
                            content=f"Function '{self._function_name}' was executed.",
                            source="MyFunctionCallTermination",
                        )
        return None

    async def reset(self) -> None:
        self._terminated = False

    def _to_config(self) -> MyFunctionCallTerminationConfig:
        return MyFunctionCallTerminationConfig(
            function_name=self._function_name,
        )

    @classmethod
    def _from_config(cls, config: MyFunctionCallTerminationConfig) -> Self:
        return cls(
            function_name=config.function_name,
        )
