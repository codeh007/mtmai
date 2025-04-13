import logging
import urllib.request

from google.adk.tools import ToolContext

logger = logging.getLogger(__name__)


def fetch_page_tool(url: str, tool_context: ToolContext) -> dict[str, str]:
    """Retrieves the content of 'url' and stores it in the ToolContext.

    Args:
        url: URL to fetch.
        tool_context: ToolContext object.

    Returns:
        A dict with "status" and (optional) "error_message" keys.
    """
    opener = urllib.request.build_opener()
    opener.addheaders = [("User-Agent", "Mozilla/5.0")]
    urllib.request.install_opener(opener)
    logger.debug("Fetching page: %s", url)
    try:
        page = urllib.request.urlopen(url)
        page_text = page.read().decode("utf-8")
    except urllib.error.HTTPError as err:
        errmsg = "Failed to fetch page %s: %s", url, err
        logger.error(errmsg)
        return {"status": "ERROR", "message": errmsg}
    tool_context.state.update({"page_contents": page_text})

    tool_context.save_artifact(filename="page_contents.txt", artifact=page_text)
    return {"status": "OK"}
