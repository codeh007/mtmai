import logging
from textwrap import dedent
from typing import Annotated

import httpx
from langchain_core.tools import tool
from langgraph.prebuilt import InjectedState

from mtmai.core.config import settings

logger = logging.getLogger()

search_result_limit = 1


@tool(response_format="content_and_artifact")
def search_tool(query: str, state: Annotated[dict, InjectedState]):  # noqa: ARG001
    """Useful to search content from web."""
    searxng_url = f"{settings.SEARXNG_URL_BASE}/search"
    logger.info("调用 search ( %s ), %s", searxng_url, query)

    with httpx.Client() as client:
        params = {"q": query, "format": "json"}
        r = client.get(searxng_url, params=params)
        # r.raise_for_status()

        if r.status_code == 429:
            return ("大模型调用每分钟token数量限制, 请在1分钟后重试", {})
        r.raise_for_status()

        search_results = r.json()

        result_list2 = search_results.get("results", [])[:search_result_limit]

        result_list3 = [
            {
                "title": x.get("title", ""),
                "url": x.get("url", ""),
                "content": x.get("content", ""),
            }
            for x in result_list2
        ]

        content_lines = ["搜索结果:"]
        for x in result_list3:
            content_lines.append(
                dedent(f"""title: {x.get("title")}
                      content: {x.get("content")}
                      """)
            )

        return (
            "\n".join(content_lines),
            {
                "artifaceType": "ArtifactSearchResults",
                "props": {
                    "title": f"{query}的搜索结果",
                    "results": result_list3,
                    "suggestions": search_results.get("suggestions", []),
                    # "infoboxes": search_results.get("infoboxes", []),
                },
            },
        )
