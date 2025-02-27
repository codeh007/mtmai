from __future__ import annotations

from mtmai import loader
from mtmai.core.config import settings
from mtmai.hatchet import Hatchet

mtmapp = Hatchet.from_config(
    loader.ConfigLoader().load_client_config(
        loader.ClientConfig(
            server_url=settings.GOMTM_URL,
            # 绑定 python 默认logger,这样,就可以不用依赖 hatchet 内置的ctx.log()
            # logger=logger,
        )
    ),
    # debug=True,
)


async def run_worker():
    # global mtmapp
    # maxRetry = settings.WORKER_MAX_RETRY
    # for i in range(maxRetry):
    #     try:
    await mtmapp.boot()
    # 确保 durable 函数注册发送在 mtmapp.worker()函数之前.
    from mtmai.flows.flow_dur import my_durable_func  # noqa

    worker = mtmapp.worker(settings.WORKER_NAME)
    # await setup_hatchet_workflows(mtmapp, worker)
    from mtmai.flows.flow_ag import FlowAg

    worker.register_workflow(FlowAg())
    # worker.register_workflow(FlowBrowser())

    # logger.info("connect gomtm server success")

    # except Exception as e:
    #     if i == maxRetry - 1:
    #         sys.exit(1)
    #     logger.info(f"failed to connect gomtm server, retry {i + 1},err:{e}")
    #     # raise e
    #     await asyncio.sleep(settings.WORKER_INTERVAL)
    # 非阻塞启动(注意: eventloop, 如果嵌套了,可能会莫名其妙的退出)
    # self.worker.setup_loop(asyncio.new_event_loop())
    # asyncio.create_task(self.worker.async_start())
    # 阻塞启动
    await worker.async_start()
