import warnings
from typing import Any

from autogen_core import ClosureAgent, MessageContext
from autogen_core.exceptions import CantHandleException


class ClosureCloser(ClosureAgent):
    def __init__(self):
        super().__init__()

    async def on_message_impl(self, message: Any, ctx: MessageContext) -> Any:
        if type(message) not in self._expected_types:
            if self._unknown_type_policy == "warn":
                warnings.warn(
                    f"Message type {type(message)} not in target types {self._expected_types} of {self.id}. Set unknown_type_policy to 'error' to raise an exception, or 'ignore' to suppress this warning.",
                    stacklevel=1,
                )
                return None
            elif self._unknown_type_policy == "error":
                raise CantHandleException(
                    f"Message type {type(message)} not in target types {self._expected_types} of {self.id}. Set unknown_type_policy to 'warn' to suppress this exception, or 'ignore' to suppress this warning."
                )

        return await self._closure(self, message, ctx)
