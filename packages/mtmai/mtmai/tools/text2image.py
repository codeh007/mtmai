# from mtmai.core.config import settings
# from mtmai.mtlibs.instagrapi import Client
import urllib.parse

import httpx
from google.adk.tools import ToolContext


# 免费的文生图 api: https://github.com/pollinations/pollinations
def text2image_tool(text: str, tool_context: ToolContext):
  """
  根据文本生成图片
  """
  getParams = {
    "model": "flux",
    "width": "1024",
    "height": "1024",
    "nologo": "true",
    "safe": "false",  # 这个参数还需要斟酌
    "enhance": "false",
    "seed": "2216940475",
  }
  apiUrl = f"https://image.pollinations.ai/prompt/{text}?{urllib.parse.urlencode(getParams)}"
  try:
    response = httpx.get(apiUrl)
    if response.status_code == 200:
      return f"生成图片成功, 图片url: {apiUrl}"
    else:
      return f"生成图片失败, 错误信息: {response.text}"
  except Exception as e:
    return f"生成图片失败, 错误信息: {e}"


async def image2text_tool(image_url: str, tool_context: ToolContext):
  """
  根据图片生成文本(提示词反推)
  """
  return "根据图片生成文本(提示词反推)的功能暂时未实现"
