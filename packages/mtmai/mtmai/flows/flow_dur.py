from typing import Any, cast

from mtmai.context.context import Context
from mtmai.mtlibs.callable import DurableContext
from mtmai.worker_app import mtmapp
from pydantic import BaseModel


class MyResultType(BaseModel):
    value: str


@mtmapp.function()
def my_func(context: Context) -> MyResultType:
    return MyResultType(value="testing123")


@mtmapp.durable()
async def my_durable_func(context: DurableContext) -> dict[str, MyResultType | None]:
    """
    解释:
        durable 修饰器似乎不是持久运行,而更像是函数的动态调用.
        例子:
            aaa = hatctx.admin.run(my_durable_func, {"test": "test-durable"})

            调用后,会产生了一次 my_durable_func 的调用,而 my_durable_func 内部又调用子工作流 my_func, 可以通过 UI反应出这个关系

    """
    result = cast(dict[str, Any], await context.run(my_func, {"test": "test"}).result())

    context.log(result)

    return {"my_durable_func": result.get("my_func")}
