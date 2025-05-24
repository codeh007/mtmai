import os
import time
from datetime import datetime
from typing import AsyncGenerator, List, override

from google.adk.agents import LlmAgent
from google.adk.agents.invocation_context import InvocationContext
from google.adk.events import Event, EventActions
from google.adk.tools.agent_tool import AgentTool
from google.genai import types  # noqa
from mtmai.agents.open_deep_research.open_deep_research import AdkOpenDeepResearch
from mtmai.agents.shortvideo_agent.shortvideo_prompts import SHORTVIDEO_PROMPT
from mtmai.agents.shortvideo_agent.sub_agents.video_terms_agent import video_terms_agent
from mtmai.model_client import get_default_litellm_model
from mtmai.mtlibs.adk_utils.callbacks import rate_limit_callback
from pydantic import BaseModel, Field

# 测试用例:
# 我想创作一个基于 nextjs 的简单的 todolist 网站,使用典型的 nextjs 技术站, 使用 tailwindcss, 数据库使用 postgresql 16


class ProductManagerState(BaseModel):
  id: str = Field(default="1")
  current_date: str = Field(default=datetime.now().strftime("%Y-%m-%d"))
  # 用户输入的初始想法
  idea: str = Field(default="")


class ProductManagerAgent(LlmAgent):
  model_config = {"arbitrary_types_allowed": True}

  def __init__(
    self,
    name: str,
    description: str = "产品经理",
    sub_agents: List[LlmAgent] = [],
    model: str = get_default_litellm_model(),
    **kwargs,
  ):
    super().__init__(
      name=name,
      description=description,
      model=model,
      instruction=SHORTVIDEO_PROMPT,
      tools=[
        # AgentTool(video_subject_generator),
        # AgentTool(video_script_agent),
        AgentTool(video_terms_agent),
        # combin_video_tool,
        # speech_tool,
        # long_running_tool,
      ],
      sub_agents=sub_agents,
      **kwargs,
    )

  async def _init_state(self, ctx: InvocationContext):
    user_content = ctx.user_content
    user_input_text = user_content.parts[0].text

    state = ctx.session.state.get("shortvideo_state")
    if state is None:
      state = ProductManagerState(
        id=ctx.session.id,
        idea=user_input_text,
      ).model_dump()
      # --- 创建带有 Actions 的事件 ---
      actions_with_update = EventActions(state_delta=state)
      # 此事件可能代表内部系统操作，而不仅仅是智能体响应
      system_event = Event(
        invocation_id="inv_book_writer_update",
        author="system",  # 或 'agent', 'tool' 等
        actions=actions_with_update,
        timestamp=time.time(),
        # content 可能为 None 或表示所采取的操作
      )
      ctx.session_service.append_event(ctx.session, system_event)
    os.makedirs(state["output_dir"], exist_ok=True)
    return state

  @override
  async def _run_async_impl(self, ctx: InvocationContext) -> AsyncGenerator[Event, None]:
    init_state = await self._init_state(ctx)
    async for event in super()._run_async_impl(ctx):
      yield event


def new_pm_agent():
  return ProductManagerAgent(
    model=get_default_litellm_model(),
    name="shortvideo_generator",
    description="产品经理",
    sub_agents=[
      # new_research_agent(),
      AdkOpenDeepResearch(
        name="open_deep_research",
        description="社交媒体话题调研专家",
        model=get_default_litellm_model(),
      ),
    ],
    before_model_callback=[rate_limit_callback],
  )
