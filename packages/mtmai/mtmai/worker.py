import asyncio
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

class WorkerApp:
    def __init__(self, backend_url: str | None):
        self.backend_url = backend_url
        if not self.backend_url:
            raise ValueError("backend_url is not set")
        self.log = structlog.get_logger()
        
        
    async def setup(self):
        global wfapp
        
        self.api_client= ApiClient(
            configuration=Configuration(
                host=self.backend_url,
            )
        )
        
        maxRetry = 10
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
                cc = config_loader.load_client_config(
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
                    )
                )
                wfapp = Hatchet.from_config(cc, debug=True)
                return wfapp
            except Exception as e:
                self.log.error(f"failed to create hatchet: {e}")
                if i == maxRetry - 1:
                    sys.exit(1)
                sleep(interval)
        raise ValueError("failed to connect gomtm server")
        


    async def deploy_mtmai_workers(self):
        await self.setup()
        self.log.info("start worker")
        worker = wfapp.worker("pyworker")
        if not worker:
            raise ValueError("worker not found")
        from mtmai.workflows.flow_router import FlowRouter

        worker.register_workflow(FlowRouter())
        # from mtmai.workflows.flow_joke_graph import PyJokeFlow

        # worker.register_workflow(PyJokeFlow())

        # from mtmai.workflows.flow_postiz import PostizFlow

        # worker.register_workflow(PostizFlow())

        # from mtmai.workflows.flow_scrape import ScrapFlow

        # worker.register_workflow(ScrapFlow())

        # from mtmai.workflows.graphflowhelper import build_graph_flow
        from mtmai.workflows.flow_crewai import FlowCrewAIAgent

        worker.register_workflow(FlowCrewAIAgent())
        
        from mtmai.workflows.flow_browser import FlowBrowser
        worker.register_workflow(FlowBrowser())
        await worker.async_start()

        while True:
            await asyncio.sleep(1)
