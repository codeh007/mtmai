# 备忘:
# https://serper.dev/api-key


from textwrap import dedent

import httpx
from langchain_community.utilities import DuckDuckGoSearchAPIWrapper
from loguru import logger
from mtmai.core.config import settings

search_engine = "duckduckgo"  # "serper" | "searxng" | "duckduckgo"


def search_web_tool(query: str) -> str:
    logger.info(f"调用搜索:{query}")

    results_limit = 10
    if search_engine == "searxng":
        return _search_searxng(query)
    elif search_engine == "duckduckgo":
        return _search_duckduckgo(query)
    elif search_engine == "serper":
        return _search_serper(query)


def _search_serper(query: str) -> str:
    return "serper 功能暂未提供"


def _search_searxng(query: str) -> str:
    searxng_url = f"{settings.SEARXNG_URL_BASE}/search"
    logger.info("调用 search ( %s ), %s", searxng_url, query)

    with httpx.Client() as client:
        params = {"q": query, "format": "json"}
        r = client.get(searxng_url, params=params)
        r.raise_for_status()

        search_results = r.json()

        result_list2 = search_results.get("results", [])[:results_limit]

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


def _search_duckduckgo(query: str) -> str:
    search_engine = DuckDuckGoSearchAPIWrapper()
    results = search_engine._ddgs_text(query)
    return [{"content": r["body"], "url": r["href"]} for r in results]
