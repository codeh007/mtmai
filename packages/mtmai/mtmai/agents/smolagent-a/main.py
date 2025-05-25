import asyncio

from smolagents import CodeAgent, InferenceClientModel, WebSearchTool, tool


@tool
def get_manual() -> str:
  """
  获取操作指引
  """
  return """
当前环境提供了一些可以直接导入的自定义库, 例如, 这里的 hello 函数, 可以直接导入使用.
```python
from mtmai.demo_code.hello import hello
some_result = hello()
```
"""


async def run_smolagent_1(task: str):
  model = InferenceClientModel()
  agent = CodeAgent(
    tools=[WebSearchTool(), get_manual],
    model=model,
    stream_outputs=True,
    additional_authorized_imports=["*"],
    max_steps=12,
    planning_interval=4,
  )

  return agent.run(task)


if __name__ == "__main__":
  asyncio.run(
    run_smolagent_1("""
你可以在当前环境执行任何代码,包括任何 shell 命令,和任何python 代码,所以,解决问题时,可以放开手脚,大胆去做.

**提示**
如果你不知道怎么做, 可以调用 **get_manual** 工具获取操作指引

**约束**
  整个过程,应该使用中文,包括思考步骤,代码生成,最终答复等.都必须使用中文.

**任务**
  现在,你使用 python 代码, 调用这个 hello 函数, 告诉我函数的返回结果



  """)
  )
