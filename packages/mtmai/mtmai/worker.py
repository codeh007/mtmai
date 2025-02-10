import logging
import os
import sys
from time import sleep

import structlog
from mtmaisdk import ClientConfig, Hatchet, loader
from mtmaisdk.clients.rest import ApiClient
from mtmaisdk.clients.rest.api.mtmai_api import MtmaiApi
from mtmaisdk.clients.rest.configuration import Configuration

from mtmai.core.config import settings

wfapp: Hatchet = None

root_logger = logging.getLogger()


class WorkerApp:
    def __init__(self):
        self.backend_url = settings.GOMTM_URL
        if not self.backend_url:
            raise ValueError("backend_url is not set")
        self.log = structlog.get_logger()
        self.worker = None  # 添加 worker 属性以便后续停止

    async def setup(self):
        global wfapp

        self.api_client = ApiClient(
            configuration=Configuration(
                host=self.backend_url,
            )
        )

        maxRetry = 50
        interval = 5
        for i in range(maxRetry):
            try:
                self.log.info("connectting...")
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
                        logger=root_logger,
                    )
                )
                wfapp = Hatchet.from_config(
                    clientConfig,
                    debug=True,
                )
                return wfapp
            except Exception as e:
                self.log.error(f"failed to create hatchet: {e}")
                if i == maxRetry - 1:
                    sys.exit(1)
                sleep(interval)
        raise ValueError("failed to connect gomtm server")

    def get_worker_name(self):
        return "pyworker"

    async def deploy_mtmai_workers(self):
        try:
            self.log.info("worker setup")
            await self.setup()
            self.log.info("start worker")
            self.worker = wfapp.worker(self.get_worker_name())

            # from mtmai.workflows.flow_crewai import FlowCrewAIAgent

            # worker.register_workflow(FlowCrewAIAgent())

            self.log.info("register flow_browser")
            from mtmai.workflows.flow_browser import FlowBrowser

            self.worker.register_workflow(FlowBrowser())

            self.log.info("register flow_tenant")
            from workflows.flow_tenant import FlowTenant

            self.worker.register_workflow(FlowTenant())

            self.log.info("register flow_ag")
            from workflows.flow_ag import FlowAg

            self.worker.register_workflow(FlowAg())

            await self.worker.async_start()

            self.log.info("start worker finished")
        except Exception as e:
            self.log.error(f"failed to deploy workers: {e}")
            raise e

    async def stop(self):
        """停止 worker"""
        if self.worker:
            self.log.info("stopping worker")
            await self.worker.async_stop()
            self.log.info("worker stopped")
