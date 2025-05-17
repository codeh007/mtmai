import time

import httpx
from loguru import logger
from smolagents import ActionStep, CodeAgent, ToolCallingAgent, WebSearchTool, tool

from mtmai.model_client import get_default_smolagents_model

# @tool
# def coding_guide(doc_path: str = "./index.md") -> str:
#   """执行前必须调用此工具,获取编写代码的指南, 并且严格遵守返回的描述进行后续的代码编写

#   Args:
#       doc_path: 文档路径, 默认是当前目录下的 index.md, 可以使用linux path 语法获取其他文档,例如: ./some_doc.md

#   Returns:
#       编写代码风格,约束,技巧,规范等描述
#   """
#   doc_root = Path(__file__).parent.parent.parent.parent / "docs"
#   with open(doc_root / "index.md", "r", encoding="utf-8") as f:
#     return f.read()


@tool
def fetch_url_raw(url: str) -> str:
  """
  访问给定的url, 并返回url的内容
  Args:
    url: 要访问的url
  Returns:
    返回 网页的 原始内容
  """
  response = httpx.get(url)
  return response.text


def save_screenshot(memory_step: ActionStep, agent: CodeAgent) -> None:
  time.sleep(1.0)  # Let JavaScript animations happen before taking the screenshot
  # driver = helium.get_driver()
  # current_step = memory_step.step_number
  # if driver is not None:
  #     for previous_memory_step in agent.memory.steps:  # Remove previous screenshots from logs for lean processing
  #         if isinstance(previous_memory_step, ActionStep) and previous_memory_step.step_number <= current_step - 2:
  #             previous_memory_step.observations_images = None
  #     png_bytes = driver.get_screenshot_as_png()
  #     image = PIL.Image.open(BytesIO(png_bytes))
  #     print(f"Captured a browser screenshot: {image.size} pixels")
  #     memory_step.observations_images = [image.copy()]  # Create a copy to ensure it persists, important!

  # # Update observations with current URL
  # url_info = f"Current url: {driver.current_url}"
  # memory_step.observations = (
  #     url_info if memory_step.observations is None else memory_step.observations + "\n" + url_info
  # )
  # return


async def run():
  from smolagents import CodeAgent

  web_agent = ToolCallingAgent(
    tools=[WebSearchTool()],
    model=get_default_smolagents_model(),
    max_steps=10,
    name="search",
    description="Runs web searches for you. Give it your query as an argument.",
  )
  manager_agent = CodeAgent(
    tools=[fetch_url_raw],
    model=get_default_smolagents_model(),
    managed_agents=[web_agent],
    additional_authorized_imports=["*"],
    max_steps=25,
    step_callbacks=[save_screenshot],
  )

  result = manager_agent.run("浏览 http://localhost:3600/api/guid 并严格按照返回的提示执行任务")
  logger.info(f"result: {result}")
