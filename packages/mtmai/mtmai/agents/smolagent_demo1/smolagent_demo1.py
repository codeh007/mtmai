from loguru import logger
from smolagents import ToolCallingAgent, WebSearchTool, tool

from mtmai.model_client import get_default_smolagents_model


@tool
def coding_guide() -> str:
  """执行前必须调用此工具,获取编写代码的指南, 并且严格遵守返回的描述进行后续的代码编写

  Returns:
      编写代码风格,约束,技巧,规范等描述
  """
  return "当编写 html 文件时, 必须添加css 样式, 系统已经内置支持 tailwindcss ^4.0.0 的语法"


async def run():
  from smolagents import CodeAgent

  # web_agent = ToolCallingAgent(
  #   tools=[coder_guide],
  #   model=get_default_smolagents_model(),
  #   max_steps=10,
  #   name="coder_guide",
  #   description="编写代码的指南",
  # )

  web_agent = ToolCallingAgent(
    tools=[WebSearchTool()],
    model=get_default_smolagents_model(),
    max_steps=10,
    name="search",
    description="Runs web searches for you. Give it your query as an argument.",
  )
  manager_agent = CodeAgent(
    tools=[coding_guide],
    model=get_default_smolagents_model(),
    managed_agents=[web_agent],
    additional_authorized_imports=["*"],
  )

  result = manager_agent.run(
    "If LLM training continues to scale up at the current rhythm until 2030, what would be the electric power in GW required to power the biggest training runs by 2030? What would that correspond to, compared to some countries? Please provide a source for any numbers used. finnal report show in html format"
  )
  logger.info(f"result: {result}")
