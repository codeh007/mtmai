from textwrap import dedent

import httpx
import structlog
from langchain_community.utilities.duckduckgo_search import DuckDuckGoSearchAPIWrapper
from langchain_core.tools import tool
from mtmai.core.config import settings

LOG = structlog.get_logger()


@tool("search_engine")
def search_engine(query: str, results_limit: int = 3, search_engine: str = "ddg"):
    """Search engine to the internet, 可选搜索引擎名称: ddg | searxng"""

    LOG.info(f"调用搜索:{search_engine},limit: {results_limit} {query}")

    if search_engine == "searxng":
        searxng_url = f"{settings.SEARXNG_URL_BASE}/search"
        LOG.info("调用 search ( %s ), %s", searxng_url, query)

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

    search_engine = DuckDuckGoSearchAPIWrapper()
    results = search_engine._ddgs_text(query)
    return [{"content": r["body"], "url": r["href"]} for r in results]
    return [{"content": r["body"], "url": r["href"]} for r in results]
