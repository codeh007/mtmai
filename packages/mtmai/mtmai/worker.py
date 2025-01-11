import asyncio
import os
import sys
from time import sleep

import structlog
from mtmai.core.config import settings
from mtmai.core.coreutils import is_in_dev
from mtmaisdk import ClientConfig, Hatchet, loader

LOG = structlog.get_logger()


def new_hatchat(backend_url: str | None) -> Hatchet:
    maxRetry = 10
    interval = 5
    if backend_url:
        settings.GOMTM_URL = backend_url

    for i in range(maxRetry):
        try:
            LOG.info("worker 连接服务器", backend_url=backend_url)
            # 不验证 tls 因后端目前 证数 是自签名的。
            os.environ["HATCHET_CLIENT_TLS_STRATEGY"] = "none"
            if not settings.HATCHET_CLIENT_TOKEN:
                raise ValueError("HATCHET_CLIENT_TOKEN is not set")
            os.environ["HATCHET_CLIENT_TOKEN"] = settings.HATCHET_CLIENT_TOKEN

            settings.MTMAI_DATABASE_URL

            # cc= ClientConfig()
            tls_config = loader.ClientTLSConfig(
                tls_strategy="none",
                cert_file="None",
                key_file="None",
                ca_file="None",
                server_name="localhost",
            )

            config_loader = loader.ConfigLoader(".")
            cc = config_loader.load_client_config(
                ClientConfig(
                    # 提示 client token 本身已经包含了服务器地址（host_port）信息
                    server_url=settings.GOMTM_URL,
                    host_port="0.0.0.0:7070",
                    tls_config=tls_config,
                )
            )

            # 原本的加载器 绑定了 jwt 中的信息，这里需要重新设置
            wfapp = Hatchet.from_config(cc, debug=True)

            return wfapp
        except Exception as e:
            LOG.error(f"failed to create hatchet: {e}")
            if i == maxRetry - 1:
                sys.exit(1)
            sleep(interval)
    raise ValueError("failed to create hatchet")


wfapp: Hatchet = new_hatchat(settings.GOMTM_URL)


class WorkerApp:
    def __init__(self, backend_url: str | None):
        self.backend_url = backend_url
        self.wfapp = new_hatchat(backend_url)

    async def setup(self):
        # from langgraph.checkpoint.postgres.aio import AsyncPostgresSaver
        # if not settings.MTMAI_DATABASE_URL:
        #     raise ValueError("MTMAI_DATABASE_URL is not set")
        # LOG.info("setup checkpoint", mtmai_database_url=settings.MTMAI_DATABASE_URL)
        # async with AsyncPostgresSaver.from_conn_string(
        #     settings.MTMAI_DATABASE_URL
        # ) as saver:
        #     await saver.setup()
        os.environ["DISPLAY"] = ":1"
        # os.environ["HATCHET_CLIENT_TOKEN"] = settings.HATCHET_CLIENT_TOKEN

    async def deploy_mtmai_workers(self, backend_url: str):
        await self.setup()
        # 获取配置文件
        # response = httpx.get("http://localhost:8383/api/v1/worker/config")
        # hatchet = Hatchet(debug=True)
        # list: WorkflowList = await wfapp.rest.aio.default_api.worker_config()
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
        # for graph in get_graphs():
        #     builded_graph = await graph.build_graph()
        #     graph_flow = await build_graph_flow(builded_graph)
        #     worker.register_workflow(graph_flow())
        if is_in_dev():
            # asyncio.create_task(setup())
            pass
        await worker.async_start()

        while True:
            await asyncio.sleep(1)
