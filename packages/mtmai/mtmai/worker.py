import asyncio
import json
import logging
import os
import sys
from typing import cast
import httpx
from mtmaisdk import ClientConfig, Hatchet, loader
from mtmaisdk.clients.rest import ApiClient
from mtmaisdk.clients.rest.api.mtmai_api import MtmaiApi
from mtmaisdk.clients.rest.configuration import Configuration
from autogen_core import Component, DefaultTopicId, SingleThreadedAgentRuntime, TopicId, TypeSubscription, try_get_known_serializers_for_type
from autogen_ext.runtimes.grpc import GrpcWorkerAgentRuntime
from mtmai.core.config import settings
from autogen_core import (
    AgentId,
    DefaultSubscription,
    DefaultTopicId,
    MessageContext,
    RoutedAgent,
    message_handler,
    default_subscription,
)
from mtmaisdk.worker.worker import Worker

from .agents.tenant_agent import TenantAgent
from mtmaisdk.clients.rest.models.tenant_seed_req import TenantSeedReq

from .agents.webui_agent import UIAgent

from .agents.ctx import AgentContext, get_mtmai_context, init_mtmai_context
from mtmaisdk.context.context import Context
from mtmaisdk.clients.rest.models.agent_run_input import AgentRunInput

from .agents._types import CascadingMessage, MessageChunk
from mtmai.agents._agents import ReceiveAgent, WorkerMainAgent
from mtmai.agents._types import CascadingMessage
from rich.console import Console
from rich.markdown import Markdown
from pydantic import BaseModel


logger = logging.getLogger()
class WorkerAppConfig(BaseModel):
    backend_url: str
class WorkerApp(Component[WorkerAppConfig]):
    def __init__(self):
        # super().__init__("worker_agent")
        self.backend_url = settings.GOMTM_URL
        if not self.backend_url:
            raise ValueError("backend_url is not set")
        self.worker = None
        self.autogen_host = None
        self.wfapp = None
        self.api_client = ApiClient(
            configuration=Configuration(
                host=self.backend_url,
            )
        )
        # Flag to track if the group chat has been initialized.
        self._initialized = False

        # Flag to track if the group chat is running.
        self._is_running = False
        self.setup_runtime()
        self.setup_agents()
    def setup_runtime(self):
        # runtime = SingleThreadedAgentRuntime()
        # grpc_runtime = GrpcWorkerAgentRuntime(host_address=settings.AG_HOST_ADDRESS)

        # grpc_runtime.start()
        # ui_agent_type = await UIAgent.register(
        #     grpc_runtime,
        #     "ui_agent",
        #     lambda: UIAgent(
        #         on_message_chunk_func=send_cl_stream,
        #     ),
        # )
        # await grpc_runtime.add_subscription(
        #     TypeSubscription(topic_type="uiagent", agent_type=ui_agent_type.type)
        # )  # TODO: This could be a great example of using agent_id to route to sepecific element in the ui. Can replace MessageChunk.message_id

        # grpc_runtime.add_message_serializer(try_get_known_serializers_for_type(CascadingMessage))

        # await grpc_runtime.publish_message(CascadingMessage(round=1), topic_id=DefaultTopicId())

        # # await grpc_runtime.stop_when_idle()
        self._runtime = SingleThreadedAgentRuntime()
    def setup_agents(self):
        WorkerMainAgent.register(self._runtime, "worker_main_agent", lambda: WorkerMainAgent(max_rounds=10))
    async def run(self):
        maxRetry = settings.WORKER_MAX_RETRY
        for i in range(maxRetry):
            try:
                mtmaiapi = MtmaiApi(self.api_client)
                workerConfig = await mtmaiapi.mtmai_worker_config()
                os.environ["HATCHET_CLIENT_TLS_STRATEGY"] = "none"
                os.environ["HATCHET_CLIENT_TOKEN"] = workerConfig.token
                os.environ["DISPLAY"] = ":1"
                config_loader = loader.ConfigLoader(".")
                clientConfig = config_loader.load_client_config(
                    ClientConfig(
                        server_url=settings.GOMTM_URL,
                        host_port=workerConfig.grpc_host_port,
                        tls_config=loader.ClientTLSConfig(
                            tls_strategy="none",
                            cert_file="None",
                            key_file="None",
                            ca_file="None",
                            server_name="localhost",
                        ),
                        # 绑定 python 默认logger,这样,就可以不用依赖 hatchet 内置的ctx.log()
                        logger=logger,
                    )
                )
                self.wfapp = Hatchet.from_config(
                    clientConfig,
                    debug=True,
                )

                self.worker = self.wfapp.worker(settings.WORKER_NAME)
                await self.setup_hatchet_workflows()

                logger.info("connect gomtm server success")
                break

            except Exception as e:
                if i == maxRetry - 1:
                    sys.exit(1)
                logger.info(f"failed to connect gomtm server, retry {i+1},err:{e}")
                await asyncio.sleep(settings.WORKER_INTERVAL)

        await self.start_autogen_host()
        # self.runtime = GrpcWorkerAgentRuntime(host_address=settings.AG_HOST_ADDRESS)
        # self.runtime.add_message_serializer(try_get_known_serializers_for_type(CascadingMessage))
        # await self.runtime.start()
        self._runtime.start()
        self._is_running=True

        # Create a new event loop but don't block on it
        loop = asyncio.new_event_loop()
        self.worker.setup_loop(loop)
        asyncio.create_task(self.worker.async_start())
        logger.info("worker started")

    @message_handler
    async def on_new_message(self, message: CascadingMessage, ctx: MessageContext) -> None:
        print(message)
        # await self.publish_message(
        #     ReceiveMessageEvent(round=message.round, sender=str(ctx.sender), recipient=str(self.id)),
        #     topic_id=DefaultTopicId(),
        # )
        # if message.round == self.max_rounds:
        #     return
        # await self.publish_message(CascadingMessage(round=message.round + 1), topic_id=DefaultTopicId())

    async def start_autogen_host(self):
        from autogen_ext.runtimes.grpc import GrpcWorkerAgentRuntimeHost
        self.autogen_host = GrpcWorkerAgentRuntimeHost(address=settings.AG_HOST_ADDRESS)
        self.autogen_host.start()
        logger.info(f"🟢 AG host at: {settings.AG_HOST_ADDRESS}")


    async def stop(self):
        if self.worker:
            await self.worker.async_stop()
            if self.autogen_host:
                await self.autogen_host.stop()
            if self.runtime:
                await self.runtime.stop()
            logger.warning("worker and autogen host stopped")


    async def setup_hatchet_workflows(self):
        logger.info("Setting up hatchet workflows...")
        wfapp = self.wfapp
        worker_app = self
        @wfapp.workflow(
            name="ag",
            on_events=["ag:run"],
            input_validator=AgentRunInput,
        )
        class FlowAg:
            @self.wfapp.step(
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

                # await grpc_runtime.stop()

                worker_app._runtime.publish_message(CascadingMessage(round=1), topic_id=DefaultTopicId())
                return {"result": "success"}

        self.worker.register_workflow(FlowAg())


        @wfapp.workflow(
            name="tenant",
            on_events=["tenant:run"],
            input_validator=TenantSeedReq,
        )
        class FlowTenant:
            """
            租户工作流
            """

            @self.wfapp.step(
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
        self.worker.register_workflow(FlowTenant())

    async def _setup_scrape_workflows(self):

        @self.wfapp.workflow(
            name="scrape", on_events=["scrape:run"], input_validator=ScrapeGraphParams
        )
        class ScrapFlow:
            @self.wfapp.step(timeout="20m", retries=2)
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
        self.worker.register_workflow(ScrapFlow())

    async def setup_browser_workflows(self):

        @self.wfapp.workflow(
            on_events=["browser:run"],
            # input_validator=CrewAIParams,
        )
        class FlowBrowser:
            @self.wfapp.step(timeout="10m", retries=1)
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
        self.worker.register_workflow(FlowBrowser())


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