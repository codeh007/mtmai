from typing import Any, Type

from pydantic import BaseModel

from mtmai.deps import AsyncSessionDep, CurrentUser


class FlowBase:
    @classmethod
    async def execute(cls) -> Any:
        raise NotImplementedError("Subclasses must implement this method")


def mtflow(form_model: Type[BaseModel]):
    def decorator(cls):
        cls.form_model = form_model
        return cls

    return decorator
