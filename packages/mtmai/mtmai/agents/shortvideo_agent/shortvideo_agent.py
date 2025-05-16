import os
import time
from datetime import datetime
from typing import Any, AsyncGenerator, List, override

from google.adk.agents import LlmAgent
from google.adk.agents.invocation_context import InvocationContext
from google.adk.events import Event, EventActions
from google.adk.tools import LongRunningFunctionTool
from google.adk.tools.agent_tool import AgentTool
from google.genai import types  # noqa
from mtmai.agents.open_deep_research.open_deep_research import AdkOpenDeepResearch
from mtmai.agents.shortvideo_agent.shortvideo_prompts import SHORTVIDEO_PROMPT
from mtmai.agents.shortvideo_agent.sub_agents.video_terms_agent import video_terms_agent
from mtmai.agents.shortvideo_agent.tools.combin_video_tool import combin_video_tool
from mtmai.agents.shortvideo_agent.tools.speech_tool import speech_tool
from mtmai.model_client import get_default_litellm_model
from mtmai.mtlibs.adk_utils.callbacks import rate_limit_callback
from pydantic import BaseModel, Field


# 1. Define the long running function
def ask_for_approval(purpose: str, amount: float) -> dict[str, Any]:
  """Ask for approval for the reimbursement."""
  # create a ticket for the approval
  # Send a notification to the approver with the link of the ticket
  return {
    "status": "pending",
    "approver": "Sean Zhou",
    "purpose": purpose,
    "amount": amount,
    "ticket-id": "approval-ticket-1",
  }


def reimburse(purpose: str, amount: float) -> str:
  """Reimburse the amount of money to the employee."""
  # send the reimbrusement request to payment vendor
  return {"status": "ok"}


# 2. Wrap the function with LongRunningFunctionTool
long_running_tool = LongRunningFunctionTool(func=ask_for_approval)


video_script_agent = LlmAgent(
  name="VideoScriptGenerator",
  model=get_default_litellm_model(),
  description="视频脚本生成专家",
  instruction="""
# Role: Video Script Generator

## Goals:
Generate a script for a video, depending on the subject of the video.

## Constrains:
1. the script is to be returned as a string with the specified number of paragraphs.
2. do not under any circumstance reference this prompt in your response.
3. get straight to the point, don't start with unnecessary things like, "welcome to this video".
4. you must not include any type of markdown or formatting in the script, never use a title.
5. only return the raw content of the script.
6. do not include "voiceover", "narrator" or similar indicators of what should be spoken at the beginning of each paragraph or line.
7. you must not mention the prompt, or anything about the script itself. also, never talk about the amount of paragraphs or lines. just write the script.
8. respond in the same language as the video subject.

# Initialization:
- number of paragraphs: {paragraph_number}
""".strip(),
  input_schema=None,
  output_key="video_script",
)


# def after_agent_callback(callback_context: CallbackContext):
#     """
#     在 agent 执行完毕后, 当ShortvideoAgent 输出 "TERMINATE" 时, 表示一切就绪,将进行最后的视频合并操作
#     """
#     if callback_context.
#     pass


class ShortvideoState(BaseModel):
  id: str = Field(default="1")
  current_date: str = Field(default=datetime.now().strftime("%Y-%m-%d"))
  title: str = Field(default="The Current State of AI in September 2024")
  topic: str = Field(default="Exploring the latest trends in AI across different industries as of September 2024")
  goal: str = Field(
    default="""
        The goal of this book is to provide a comprehensive overview of the current state of artificial intelligence in September 2024.
        It will delve into the latest trends impacting various industries, analyze significant advancements,
        and discuss potential future developments. The book aims to inform readers about cutting-edge AI technologies
        and prepare them for upcoming innovations in the field.
    """
  )
  video_subject: str = Field(default="")
  video_script: str = Field(default="")
  video_terms: List[str] = Field(default_factory=list)
  video_terms_amount: int = Field(default=3)
  audio_file: str = Field(default="")
  output_dir: str = Field(default="")
  voice_name: str = Field(default="zh-CN-XiaoxiaoNeural")
  voice_llm_provider: str = Field(default="edgetts")
  paragraph_number: int = Field(default=3)


class ShortvideoAgent(LlmAgent):
  model_config = {"arbitrary_types_allowed": True}

  def __init__(
    self,
    name: str,
    description: str = "短视频生成专家",
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
        AgentTool(video_script_agent),
        AgentTool(video_terms_agent),
        combin_video_tool,
        speech_tool,
        long_running_tool,
      ],
      sub_agents=sub_agents,
      **kwargs,
    )

  async def _init_state(self, ctx: InvocationContext):
    user_content = ctx.user_content
    user_input_text = user_content.parts[0].text

    state = ctx.session.state.get("shortvideo_state")
    if state is None:
      state = ShortvideoState(
        id=ctx.session.id,
        title=user_input_text,
        topic=user_input_text,
        goal=user_input_text,
        video_subject=user_input_text,
        video_script=user_input_text,
        paragraph_number=3,
        video_terms_amount=3,
        output_dir=f".vol/short_videos/{ctx.session.id}",
        voice_name="zh-CN-XiaoxiaoNeural",
        voice_llm_provider="edgetts",
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


def new_shortvideo_agent():
  return ShortvideoAgent(
    model=get_default_litellm_model(),
    name="shortvideo_generator",
    description="短视频生成专家",
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
