from dataclasses import dataclass
from typing import Any

from autogen_core import DefaultInterventionHandler, MessageContext


@dataclass
class Message:
    content: Any


@dataclass
class Termination:
    reason: str


class TerminationHandler(DefaultInterventionHandler):
    def __init__(self) -> None:
        self._termination_value: Termination | None = None

    async def on_publish(self, message: Any, *, message_context: MessageContext) -> Any:
        if isinstance(message, Termination):
            self._termination_value = message
        return message

    @property
    def termination_value(self) -> Termination | None:
        return self._termination_value

    @property
    def has_terminated(self) -> bool:
        return self._termination_value is not None
