from loguru import logger

from mtmai.core.config import settings
from mtmai.hatchet import Hatchet

mtmapp = Hatchet()

# ag_runtime: AgentRuntime | None = None


async def run_worker():
    await mtmapp.boot()

    global ag_runtime
    # ag_runtime = mtmapp.agent_runtime
    # ag_runtime = MtmAgentRuntime(config=mtmapp.config)

    # await ag_runtime.start()

    # await greeter_team.run("greeter_team", ag_runtime)
    # 确保 durable 函数注册发送在 mtmapp.worker()函数之前.
    # from mtmai.flows.flow_dur import my_durable_func  # noqa

    worker = mtmapp.worker(settings.WORKER_NAME)
    # await setup_hatchet_workflows(mtmapp, worker)
    from mtmai.flows.flow_ag import FlowAg

    worker.register_workflow(FlowAg())
    # worker.register_workflow(FlowBrowser())

    # 非阻塞启动(注意: eventloop, 如果嵌套了,可能会莫名其妙的退出)
    # self.worker.setup_loop(asyncio.new_event_loop())
    # asyncio.create_task(self.worker.async_start())
    # 阻塞启动
    await worker.async_start()


async def start_ag_teams():
    logger.info("STARTING AG TEAMS.------------------------------------------")
    pass
