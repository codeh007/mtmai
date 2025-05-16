import logging
import time
from datetime import datetime
from typing import AsyncGenerator, List, override

from google.adk.agents import LlmAgent
from google.adk.agents.invocation_context import InvocationContext
from google.adk.events import Event, EventActions
from google.adk.tools import ToolContext
from google.genai import types  # noqa
from mtmai.model_client import get_default_litellm_model
from mtmai.mtlibs.adk_utils.callbacks import rate_limit_callback
from mtmai.mtlibs.youtube_short_gen.Components.YoutubeDownloader import download_youtube_video
from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)


class ShortvideoDecodeState(BaseModel):
  id: str = Field(default="1")
  current_date: str = Field(default=datetime.now().strftime("%Y-%m-%d"))
  original_url: str = Field(default="")
  title: str = Field(default="The Current State of AI in September 2024")
  topic: str = Field(default="Exploring the latest trends in AI across different industries as of September 2024")


def download_video_tool(url: str, tool_context: ToolContext):
  """视频下载工具, 给定一个视频的url, 下载视频并返回视频的本地路径,并且返回视频的基本信息

  Args:
      url (str): 视频的url
      tool_context (ToolContext): 工具上下文

  Returns:
      str: 下载结果及视频的基本信息
  """
  output_file = download_youtube_video(url)
  logger.info(f"视频下载成功: {output_file}")
  tool_context.state["original_url"] = url
  return "视频下载成功"


class ShortvideoDecodeAgent(LlmAgent):
  """
  给定一个短视频(网址或者附件)，生成一个短视频的脚本
  """

  model_config = {"arbitrary_types_allowed": True}

  def __init__(
    self,
    name: str,
    description: str = "短视频解码专家",
    sub_agents: List[LlmAgent] = [],
    model: str = get_default_litellm_model(),
    **kwargs,
  ):
    super().__init__(
      name=name,
      description=description,
      model=model,
      instruction="""你是一个短视频解码及分析专家, 职责是协助用户完成短视频的分析
通常用户会给你网上的短视频网址,同时告诉你希望你对这个短视频如何分析,希望得到什么答案.
你应该充分使用现有的工具, 来完成用户的请求.
**工具**
* `download_video_tool`: 下载视频工具, 下载视频并返回视频的本地路径,并且返回视频的基本信息

""",
      tools=[download_video_tool],
      sub_agents=sub_agents,
      **kwargs,
    )

  async def _init_state(self, ctx: InvocationContext):
    user_content = ctx.user_content
    user_input_text = user_content.parts[0].text

    state = ctx.session.state.get("shortvideo_state")
    if state is None:
      state = ShortvideoDecodeState(
        id=ctx.session.id,
        title=user_input_text,
        topic=user_input_text,
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
    # os.makedirs(state["output_dir"], exist_ok=True)
    return state

  @override
  async def _run_async_impl(self, ctx: InvocationContext) -> AsyncGenerator[Event, None]:
    init_state = await self._init_state(ctx)
    async for event in super()._run_async_impl(ctx):
      yield event


def new_shortvideo_decode_agent():
  return ShortvideoDecodeAgent(
    model=get_default_litellm_model(),
    name="shortvideo_decode",
    description="短视频解码专家, 给定一个短视频(网址或者附件)，生成一段对这个视频的相关描述,例如视频的主题, 分类 之类的",
    sub_agents=[
      # new_research_agent(),
      # AdkOpenDeepResearch(
      #   name="open_deep_research",
      #   description="社交媒体话题调研专家",
      #   model=get_default_litellm_model(),
      # ),
    ],
    before_model_callback=[rate_limit_callback],
  )
