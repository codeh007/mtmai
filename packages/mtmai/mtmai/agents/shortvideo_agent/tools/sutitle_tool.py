"""字幕生成工具"""

import logging

from google.adk.tools import ToolContext

# from ..shared_libraries import file_utils

logger = logging.getLogger(__name__)


def subtitle_tool(tool_context: ToolContext) -> dict:
    """
    字幕生成工具
    """
    fed_hostname = "https://www.federalreserve.gov"
    transcript_url = tool_context.state["transcript_url"]
    if not transcript_url.startswith("https"):
        transcript_url = fed_hostname + transcript_url
    pdf_path = file_utils.download_file_from_url(
        transcript_url, "transcript.pdf", tool_context
    )
    if pdf_path is None:
        logger.error("Failed to download PDF from URLs, aborting")
        return {
            "status": "error",
            "error_message": "Failed to download PDFs from GCS",
        }

    text = file_utils.extract_text_from_pdf_artifact(pdf_path, tool_context)
    filename = "transcript_fulltext"
    version = tool_context.save_artifact(filename=filename, artifact=Part(text=text))
    logger.info("Saved artifact %s, ver %i", filename, version)
    return {"status": "ok"}
