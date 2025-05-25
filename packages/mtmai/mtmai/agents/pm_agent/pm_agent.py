import os
from datetime import datetime
from typing import Any, AsyncGenerator

from google.adk.agents import LlmAgent
from google.adk.agents.callback_context import CallbackContext
from google.adk.events import Event
from google.adk.tools import ToolContext
from google.genai import types  # noqa
from mtmai.model_client import get_default_litellm_model
from mtmai.mtlibs.adk_utils.callbacks import rate_limit_callback
from pydantic import BaseModel, Field

# 测试用例:
# 我想创作一个基于 nextjs 的简单的 todolist 网站,使用典型的 nextjs 技术站, 使用 tailwindcss, 数据库使用 postgresql 16


# 设计思路:
#    当设计一个有一定规模的应用时, 往往需要产品经理先上手, 将需求文档,用户故事,评估指标,形成文档后.
#    后续团队只需要将 需求文档, 分解成不同的任务,交给不同的团队成员一步一步执行即可.


class ProductManagerState(BaseModel):
  id: str = Field(default="1")
  current_date: str = Field(default=datetime.now().strftime("%Y-%m-%d"))

  # 产品经理手册
  pm_manual: str = Field(default="")
  # 用户输入的初始想法
  idea: str = Field(default="")


async def save_artifacts(path: str, content: str, mime_type: str, tool_context: ToolContext) -> dict[str, Any]:
  """保存构建的文档"""
  await tool_context.save_artifact(
    path,
    types.Part(text=f"保存 {path} 成功", inline_data=types.Blob(mime_type=mime_type, data=content.encode("utf-8"))),
  )
  return "ok"


async def load_pm_prompt():
  prompt_path = os.path.join(os.path.dirname(__file__), "pm_manual.md")
  with open(prompt_path, "r") as f:
    return f.read()


async def before_agent(callback_context: CallbackContext) -> AsyncGenerator[Event, None]:
  # 从 api 中加载 pm 操作手册
  callback_context.state["pm_manual"] = await load_pm_prompt()


def new_pm_agent():
  return LlmAgent(
    model=get_default_litellm_model(),
    name="product_manager",
    description="产品经理",
    instruction="""你是有10年以上经验产品经理, 请根据用户输入的初始想法, 结合产品经理手册, 生成一个产品需求文档

** 产品经理手册**

  {pm_manual}
""",
    sub_agents=[
      # new_research_agent(),
      # AdkOpenDeepResearch(
      #   name="open_deep_research",
      #   description="社交媒体话题调研专家",
      #   model=get_default_litellm_model(),
      # ),
    ],
    tools=[
      # save_artifacts,
    ],
    before_model_callback=[rate_limit_callback],
    before_agent_callback=[before_agent],
  )
