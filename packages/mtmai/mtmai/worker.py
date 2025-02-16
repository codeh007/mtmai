import asyncio
import logging
import os
import sys
from typing import cast

from autogen_core import (
    DefaultTopicId,
    SingleThreadedAgentRuntime,
    try_get_known_serializers_for_type,
)
from mtmaisdk import ClientConfig, Hatchet, loader
from mtmaisdk.clients.rest import ApiClient
from mtmaisdk.clients.rest.api.mtmai_api import MtmaiApi
from mtmaisdk.clients.rest.configuration import Configuration
from mtmaisdk.clients.rest.models.agent_run_input import AgentRunInput
from mtmaisdk.clients.rest.models.chat_message import ChatMessage
from mtmaisdk.clients.rest.models.tenant_seed_req import TenantSeedReq
from mtmaisdk.clients.rest_client import AsyncRestApi
from mtmaisdk.context.context import Context, set_api_token_context, set_backend_url

from mtmai.core.config import settings

from .agents._types import ApiSaveTeamState, ApiSaveTeamTaskResult
from .agents.hf_space_agent import HfSpaceAgent
from .agents.webui_agent import UIAgent
from .agents.worker_agent import WorkerAgent
from .mtmaisdk.client import set_gomtm_api_context
from .mtmaisdk.clients.rest.models.ag_event_create import AgEventCreate
from .mtmaisdk.clients.rest.models.chat_message_upsert import ChatMessageUpsert
from .mtmaisdk.clients.rest.models.task_result import TaskResult

logger = logging.getLogger()


class WorkerAgent:
    def __init__(self):
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
        set_backend_url(self.backend_url)
        self._initialized = False
        self._is_running = False
        self.setup_runtime()

    def setup_runtime(self):
        # from autogen_ext.runtimes.grpc import GrpcWorkerAgentRuntime
        # grpc_runtime = GrpcWorkerAgentRuntime(host_address=settings.AG_HOST_ADDRESS)
        self._runtime = SingleThreadedAgentRuntime()
        # self._runtime.add_message_serializer(try_get_known_serializers_for_type(CascadingMessage))

        message_serializer_types = [
            AgentRunInput,
            TenantSeedReq,
            ChatMessage,
            ChatMessageUpsert,
            AgEventCreate,
            TaskResult,
            ApiSaveTeamState,
            ApiSaveTeamTaskResult,
        ]
        for message_serializer_type in message_serializer_types:
            self._runtime.add_message_serializer(
                try_get_known_serializers_for_type(message_serializer_type)
            )

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
                token = clientConfig.token
                set_api_token_context(token)
                self.gomtmapi = AsyncRestApi(
                    host=settings.GOMTM_URL,
                    api_key=workerConfig.token,
                    tenant_id=clientConfig.tenant_id,
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
                logger.info(f"failed to connect gomtm server, retry {i + 1},err:{e}")
                await asyncio.sleep(settings.WORKER_INTERVAL)

        await self.start_autogen_host()
        self._runtime.start()

        await WorkerAgent.register(
            self._runtime,
            "worker_main_agent",
            lambda: WorkerAgent(gomtmapi=self.gomtmapiwfapp),
        )
        await UIAgent.register(
            self._runtime,
            "ui_agent",
            lambda: UIAgent(wfapp=self.wfapp),
        )
        await HfSpaceAgent.register(
            self._runtime,
            "hf_space_agent",
            lambda: HfSpaceAgent(
                description="hfspace_agent",
                wfapp=self.wfapp,
            ),
        )

        self._is_running = True

        # Create a new event loop but don't block on it
        loop = asyncio.new_event_loop()
        self.worker.setup_loop(loop)
        asyncio.create_task(self.worker.async_start())
        logger.info("worker started")

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
        wfapp = self.wfapp
        worker_app = self

        @wfapp.workflow(
            name="ag",
            on_events=["ag:run"],
            input_validator=AgentRunInput,
        )
        class FlowAg:
            @self.wfapp.step(timeout="30m")
            async def step_entry(self, hatctx: Context):
                set_gomtm_api_context(hatctx.aio)
                input = cast(AgentRunInput, hatctx.workflow_input())
                if not input.run_id:
                    input.run_id = hatctx.workflow_run_id()
                await worker_app._runtime.publish_message(input, DefaultTopicId())
                return {"result": "success"}

        self.worker.register_workflow(FlowAg())

    async def setup_browser_workflows(self):
        @self.wfapp.workflow(
            on_events=["browser:run"],
            # input_validator=CrewAIParams,
        )
        class FlowBrowser:
            @self.wfapp.step(timeout="10m", retries=1)
            async def run(self, hatctx: Context):
                from mtmaisdk.clients.rest.models import BrowserParams

                # from mtmai.agents.browser_agent import BrowserAgent

                input = BrowserParams.model_validate(hatctx.workflow_input())
                # init_mtmai_context(hatctx)

                # ctx = get_mtmai_context()
                # tenant_id = ctx.tenant_id
                # llm_config = await wfapp.rest.aio.llm_api.llm_get(
                #     tenant=tenant_id, slug="default"
                # )
                # llm = ChatOpenAI(
                #     model=llm_config.model,
                #     api_key=llm_config.api_key,
                #     base_url=llm_config.base_url,
                #     temperature=0,
                #     max_tokens=40960,
                #     verbose=True,
                #     http_client=httpx.Client(transport=LoggingTransport()),
                #     http_async_client=httpx.AsyncClient(transport=LoggingTransport()),
                # )

                # 简单测试llm 是否配置正确
                # aa=llm.invoke(["Hello, how are you?"])
                # print(aa)
                # agent = BrowserAgent(
                #     generate_gif=False,
                #     use_vision=False,
                #     tool_call_in_content=False,
                #     # task="Navigate to 'https://en.wikipedia.org/wiki/Internet' and scroll down by one page - then scroll up by 100 pixels - then scroll down by 100 pixels - then scroll down by 10000 pixels.",
                #     task="Navigate to 'https://en.wikipedia.org/wiki/Internet' and to the string 'The vast majority of computer'",
                #     llm=llm,
                #     browser=Browser(config=BrowserConfig(headless=False)),
                # )
                # await agent.run()

        self.worker.register_workflow(FlowBrowser())
