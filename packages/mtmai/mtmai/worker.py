import logging
import os
import sys
from time import sleep

from mtmaisdk import ClientConfig, Hatchet, loader
from mtmaisdk.clients.rest import ApiClient
from mtmaisdk.clients.rest.api.mtmai_api import MtmaiApi
from mtmaisdk.clients.rest.configuration import Configuration
from autogen_core import DefaultTopicId, try_get_known_serializers_for_type
from autogen_ext.runtimes.grpc import GrpcWorkerAgentRuntime
from mtmai.core.config import settings
from autogen_core import (
    AgentId,
    DefaultSubscription,
    DefaultTopicId,
    MessageContext,
    RoutedAgent,
    message_handler,
)

wfapp: Hatchet = None

logger = logging.getLogger()

@default_subscription
class WorkerAppAgent(RoutedAgent):
    def __init__(self):
        self.backend_url = settings.GOMTM_URL
        if not self.backend_url:
            raise ValueError("backend_url is not set")
        self.worker = None
        self.autogen_host = None

    async def setup(self):
        global wfapp

        self.api_client = ApiClient(
            configuration=Configuration(
                host=self.backend_url,
            )
        )

        maxRetry = 1000
        interval = 1
        for i in range(maxRetry):
            try:
                logger.info("connectting...")
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
                wfapp = Hatchet.from_config(
                    clientConfig,
                    debug=True,
                )
                return wfapp
            except Exception as e:
                if i == maxRetry - 1:
                    sys.exit(1)
                sleep(interval)
        raise ValueError("failed to connect gomtm server")

    async def deploy_mtmai_workers(self):
        try:
            await self.setup()
            self.worker = wfapp.worker(settings.WORKER_NAME)
            logger.info("register flow_browser")
            from mtmai.workflows.flow_browser import FlowBrowser

            self.worker.register_workflow(FlowBrowser())

            logger.info("register flow_tenant, flow_ag")
            from workflows.flow_ag import FlowAg, FlowTenant
            self.worker.register_workflow(FlowTenant())
            self.worker.register_workflow(FlowAg())
            await self.start_autogen_host()
            await self.start_reveiver_agent()
            await self.worker.async_start()

            logger.info("start worker finished")


        except Exception as e:
            logger.exception(f"failed to deploy workers: {e}")

            raise e

    async def start_autogen_host(self):
        from autogen_ext.runtimes.grpc import GrpcWorkerAgentRuntimeHost
        self.autogen_host = GrpcWorkerAgentRuntimeHost(address=settings.AG_HOST_ADDRESS)
        self.autogen_host.start()
        logger.info(f"🟢 AG host at: {settings.AG_HOST_ADDRESS}")


    async def start_reveiver_agent(self):
        """
            作用:
                作为分布式,其他 agents 运行的过程不直接处理消息的日志, 前端界面的消息处理等数据.
                这里,通过 grpc 的方式,接收其他 agents 的日志, 前端界面的消息处理等数据.
        """
        from ag.agents._agents import ReceiveAgent
        from mtmai.ag.agents._types import CascadingMessage
        self.autogen_worker_runtime = GrpcWorkerAgentRuntime(host_address=settings.AG_HOST_ADDRESS)
        self.autogen_worker_runtime.add_message_serializer(try_get_known_serializers_for_type(CascadingMessage))
        self.autogen_worker_runtime.start()

    async def stop(self):
        if self.worker:
            await self.worker.async_stop()
            if self.autogen_host:
                await self.autogen_host.stop()
            if self.autogen_worker_runtime:
                await self.autogen_worker_runtime.stop()
            logger.warning("worker and autogen host stopped")

