import logging
from datetime import datetime
from typing import AsyncGenerator, List, override

from google.adk.agents import LlmAgent
from google.adk.agents.invocation_context import InvocationContext
from google.adk.events import Event
from google.adk.tools import ToolContext
from google.genai import types  # noqa
from mtmai.model_client import get_default_litellm_model
from mtmai.mtlibs.adk_utils.callbacks import rate_limit_callback
from mtmai.mtlibs.youtube_short_gen.YoutubeDownloader import download_youtube_video
from mtmai.tools.text2image import image2text_tool, text2image_tool
from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)


class Image2ShortsState(BaseModel):
  id: str = Field(default="1")
  current_date: str = Field(default=datetime.now().strftime("%Y-%m-%d"))
  original_url: str = Field(default="")
  title: str = Field(default="The Current State of AI in September 2024")
  topic: str = Field(default="Exploring the latest trends in AI across different industries as of September 2024")


def download_image_tool(url: str, tool_context: ToolContext):
  """图片下载工具, 给定一个图片的url, 下载图片并返回图片的本地路径,并且返回图片的基本信息

  Args:
      url (str): 视频的url
      tool_context (ToolContext): 工具上下文

  Returns:
      str: 下载结果及图片的基本信息
  """
  try:
    yt = download_youtube_video(url)
    tool_context.state["original_url"] = url
    return f"视频下载成功, 视频标题: {yt.title}, 视频描述: {yt.description}, 视频时长: {yt.length}"
  except Exception as e:
    return f"图片下载失败, 错误信息: {e}"


class Image2ShortsAgent(LlmAgent):
  """
  输入一张图片, 生成一个短视频
  """

  model_config = {"arbitrary_types_allowed": True}

  def __init__(
    self,
    name: str,
    description: str = "由一张图片生成一个短视频",
    sub_agents: List[LlmAgent] = [],
    model: str = get_default_litellm_model(),
    **kwargs,
  ):
    super().__init__(
      name=name,
      description=description,
      model=model,
      instruction="""你是短视频生成专家, 职责是协助用户完成短视频的生成
用户会给你一张图片,并且告诉你具体的要求
你应该充分使用现有的工具, 来完成用户的请求.
尽你最大的努力, 使用户满意.
尽力不要询问用户, 除非用户主动告诉你

**TOOLS**
- text2image_tool: 专用的图片生成工具, 可以根据文本生成对应的图片

- image2text_tool: 专用的图片提示词反推工具, 可以根据图片生成对应的提示词,
                    生成的提示词可以直接使用 text2image ai 模型生成内容和风格接近的图片
""",
      tools=[download_image_tool, text2image_tool, image2text_tool],
      sub_agents=sub_agents,
      **kwargs,
    )

  async def _init_state(self, ctx: InvocationContext):
    user_content = ctx.user_content
    user_input_text = user_content.parts[0].text

    state = ctx.session.state.get("shortvideo_state")
    if state is None:
      state = Image2ShortsState(
        id=ctx.session.id,
        title=user_input_text,
        topic=user_input_text,
      ).model_dump()
    return state

  @override
  async def _run_async_impl(self, ctx: InvocationContext) -> AsyncGenerator[Event, None]:
    init_state = await self._init_state(ctx)
    async for event in super()._run_async_impl(ctx):
      yield event


def new_image2shorts_agent():
  return Image2ShortsAgent(
    model=get_default_litellm_model(),
    name="image2shorts",
    description="由一张图片生成一个短视频",
    sub_agents=[],
    before_model_callback=[rate_limit_callback],
  )
