"""音频生成工具"""

import logging

from google.adk.tools import ToolContext

# from ..shared_libraries import file_utils

logger = logging.getLogger(__name__)


def gen_speech_tool(tool_context: ToolContext) -> dict:
    """
    视频解说音频生成工具
    """

    return {"status": "ok"}
