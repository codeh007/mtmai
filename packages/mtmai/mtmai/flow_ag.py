import asyncio
import json
import logging
from typing import cast

import httpx
from mtmai.agents._types import MessageChunk

from mtmai.agents.webui_agent import UIAgent
from mtmaisdk.hatchet import Hatchet
from mtmaisdk.worker.worker import Worker
from agents.ctx import AgentContext
from mtmaisdk.clients.rest.models.agent_run_input import AgentRunInput
from mtmaisdk.context.context import Context
from mtmai.agents.ctx import get_mtmai_context, init_mtmai_context
from typing import cast
from autogen_ext.runtimes.grpc import GrpcWorkerAgentRuntime
from mtmai.agents.tenant_agent import TenantAgent
from mtmaisdk.clients.rest.models.tenant_seed_req import TenantSeedReq
from agents.ctx import AgentContext
from mtmaisdk.clients.rest.models.agent_run_input import AgentRunInput
from mtmaisdk.clients.rest.models.team import Team
from mtmaisdk.context.context import Context
from mtmai.agents.ctx import get_mtmai_context, init_mtmai_context
from autogen_core import  SingleThreadedAgentRuntime, TypeSubscription
from autogen_core import TopicId
from rich.console import Console
from mtmai.core.config import settings
from rich.markdown import Markdown

logger = logging.getLogger(__name__)


async def send_cl_stream(msg: MessageChunk) -> None:
    print(msg)
    # if msg.message_id not in message_chunks:
    #     message_chunks[msg.message_id] = Message(content="", author=msg.author)

    # if not msg.finished:
    #     await message_chunks[msg.message_id].stream_token(msg.text)  # type: ignore [reportUnknownVariableType]
    # else:
    #     await message_chunks[msg.message_id].stream_token(msg.text)  # type: ignore [reportUnknownVariableType]
    #     await message_chunks[msg.message_id].update()  # type: ignore [reportUnknownMemberType]
    #     await asyncio.sleep(3)
    #     cl_msg = message_chunks[msg.message_id]  # type: ignore [reportUnknownVariableType]
    #     await cl_msg.send()  # type: ignore [reportUnknownMemberType]


async def setup_hatchet_workflows(wfapp: Hatchet,worker: Worker):
    logger.info("Setting up hatchet workflows...")

    @wfapp.workflow(
        name="ag",
        on_events=["ag:run"],
        input_validator=AgentRunInput,
    )
    class FlowAg:
        @wfapp.step(
            timeout="30m",
            # retries=1
        )
        async def step_entry(self, hatctx: Context):
            init_mtmai_context(hatctx)
            input = cast(AgentRunInput, hatctx.workflow_input())
            # 旧版功能
            # team_runner = TeamRunner()
            # async for event in team_runner.run_stream(input):
            #     _event = event
            #     if isinstance(event, BaseModel):
            #         _event = event.model_dump()
            #     result = await hatctx.rest_client.aio.ag_events_api.ag_event_create(
            #         tenant=input.tenant_id,
            #         ag_event_create=AgEventCreate(
            #             data=_event,
            #             framework="autogen",
            #             stepRunId=hatctx.step_run_id,
            #             meta={},
            #         ),
            #     )
            #     # hatctx.log(result)
            #     hatctx.put_stream(event)

            # 新版功能
            # runtime = SingleThreadedAgentRuntime()
            grpc_runtime = GrpcWorkerAgentRuntime(host_address=settings.AG_HOST_ADDRESS)

            grpc_runtime.start()
            ui_agent_type = await UIAgent.register(
                grpc_runtime,
                "ui_agent",
                lambda: UIAgent(
                    on_message_chunk_func=send_cl_stream,
                ),
            )
            Console().print(Markdown("Starting **`UI Agent`**"))

            await grpc_runtime.add_subscription(
                TypeSubscription(topic_type="uiagent", agent_type=ui_agent_type.type)
            )  # TODO: This could be a great example of using agent_id to route to sepecific element in the ui. Can replace MessageChunk.message_id


            # await grpc_runtime.stop_when_idle()
            await grpc_runtime.stop()

            return {"result": "success"}

    worker.register_workflow(FlowAg())


    @wfapp.workflow(
        name="tenant",
        on_events=["tenant:run"],
        input_validator=TenantSeedReq,
    )
    class FlowTenant:
        """
        租户工作流
        """

        @wfapp.step(
            timeout="30m",
            # retries=1
        )
        async def step_reset_tenant(self, hatctx: Context):
            init_mtmai_context(hatctx)
            ctx: AgentContext = get_mtmai_context()
            ctx.set_hatch_context(hatctx)
            input = cast(TenantSeedReq, hatctx.workflow_input())
            # 新版功能
            runtime = SingleThreadedAgentRuntime()
            await TenantAgent.register(runtime, "tenant_agent", lambda: TenantAgent(ctx))
            # await runtime.add_subscription(TypeSubscription(topic_type="tenant", agent_type="broadcasting_agent"))

            runtime.start()
            # await runtime.send_message(
            #     message=input,
            #     recipient=AgentId(type="tenant_agent", key="default"),
            # )
            # 广播方从而避免工作流中消息类型的相关转换问题.
            await runtime.publish_message(
                input,
                topic_id=TopicId(type="tenant", source="tenant"),
            )

            await runtime.stop_when_idle()  # This will block until the runtime is idle.
            await runtime.close()
            return {"result": "success"}
    worker.register_workflow(FlowTenant())

def _setup_scrape_workflows(wfapp: Hatchet,worker: Worker):

    @wfapp.workflow(
        name="scrape", on_events=["scrape:run"], input_validator=ScrapeGraphParams
    )
    class ScrapFlow:
        @wfapp.step(timeout="20m", retries=2)
        async def graph_entry(self, hatctx: Context):
            # from scrapegraphai.graphs import SmartScraperGraph
            # from mtmaisdk.clients.rest.api.llm_api import LlmApi

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
    worker.register_workflow(ScrapFlow())

def setup_browser_workflows(wfapp: Hatchet,worker: Worker):

    @wfapp.workflow(
        on_events=["browser:run"],
        # input_validator=CrewAIParams,
    )
    class FlowBrowser:
        @wfapp.step(timeout="10m", retries=1)
        async def run(self, hatctx: Context):
            from mtmai.mtlibs.httpx_transport import LoggingTransport

            from browser_use.browser.browser import Browser, BrowserConfig
            from langchain_openai import ChatOpenAI
            from mtmaisdk.clients.rest.models import BrowserParams

            from mtmai.agents.browser_agent import BrowserAgent

            input = BrowserParams.model_validate(hatctx.workflow_input())
            init_mtmai_context(hatctx)

            ctx = get_mtmai_context()
            tenant_id = ctx.tenant_id
            llm_config = await wfapp.rest.aio.llm_api.llm_get(
                tenant=tenant_id, slug="default"
            )
            llm = ChatOpenAI(
                model=llm_config.model,
                api_key=llm_config.api_key,
                base_url=llm_config.base_url,
                temperature=0,
                max_tokens=40960,
                verbose=True,
                http_client=httpx.Client(transport=LoggingTransport()),
                http_async_client=httpx.AsyncClient(transport=LoggingTransport()),
            )

            # 简单测试llm 是否配置正确
            # aa=llm.invoke(["Hello, how are you?"])
            # print(aa)
            agent = BrowserAgent(
                generate_gif=False,
                use_vision=False,
                tool_call_in_content=False,
                # task="Navigate to 'https://en.wikipedia.org/wiki/Internet' and scroll down by one page - then scroll up by 100 pixels - then scroll down by 100 pixels - then scroll down by 10000 pixels.",
                task="Navigate to 'https://en.wikipedia.org/wiki/Internet' and to the string 'The vast majority of computer'",
                llm=llm,
                browser=Browser(config=BrowserConfig(headless=False)),
            )
            await agent.run()
    worker.register_workflow(FlowBrowser())
