from typing import Any, TypedDict, cast

from mtmai.context.context import Context
from mtmai.hatchet import durable, function
from mtmai.mtlibs.callable import DurableContext


class MyResultType(TypedDict):
    my_func: str


@function()
def my_func(context: Context) -> MyResultType:
    return MyResultType(my_func="testing123")


@durable()
async def my_durable_func(context: DurableContext) -> dict[str, MyResultType | None]:
    result = cast(dict[str, Any], await context.run(my_func, {"test": "test"}).result())

    context.log(result)

    return {"my_durable_func": result.get("my_func")}
