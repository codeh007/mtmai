import asyncio
import json

import structlog
from mtmai.worker import wfapp
from mtmaisdk.clients.rest.api.llm_api import LlmApi
from mtmaisdk.clients.rest.models import ScrapeGraphParams
from mtmaisdk.clients.rest_client import LogApi
from mtmaisdk.context.context import Context
from scrapegraphai.graphs import SmartScraperGraph

LOG = structlog.get_logger()


@wfapp.workflow(
    name="scrape", on_events=["scrape:run"], input_validator=ScrapeGraphParams
)
class ScrapFlow:
    @wfapp.step(timeout="20m", retries=2)
    async def graph_entry(self, hatctx: Context):
        # 获取 llm 配置
        llm_config = hatctx.rest_client.aio._api_client
        log_api = LogApi(hatctx.rest_client.aio._api_client)
        result = await log_api.log_line_list(step_run=hatctx.step_run_id)
        print(result)
        llm_api = LlmApi(hatctx.rest_client.aio._api_client)
        llm_config = await llm_api.llm_get(
            # tenant=hatctx.tenant_id,
            # slug=hatctx.node_id,
            # agent_node_run_request=hatctx.agent_node_run_request,
        )
        print(llm_config)
        # Define the configuration for the scraping pipeline
        graph_config = {
            "llm": {
                "api_key": "YOUR_OPENAI_APIKEY",
                "model": "openai/gpt-4o-mini",
            },
            "verbose": True,
            "headless": False,
        }

        # Create the SmartScraperGraph instance
        smart_scraper_graph = SmartScraperGraph(
            prompt="Extract me all the news from the website",
            source="https://www.wired.com",
            config=graph_config,
        )

        # Run the pipeline
        # result = smart_scraper_graph.run()
        result = await asyncio.to_thread(smart_scraper_graph.run)

        print(json.dumps(result, indent=4))
