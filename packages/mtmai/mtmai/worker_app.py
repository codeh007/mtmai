from loguru import logger

from mtmai.core.config import settings
from mtmai.hatchet import Hatchet

mtmapp = Hatchet()


async def run_worker():
    logger.info("booting worker")
    await mtmapp.boot()

    from mtmai.otel import setup_instrument

    setup_instrument()

    worker = mtmapp.worker(settings.WORKER_NAME)
    _start_coroutine = worker.agent_runtime.start()
    if _start_coroutine:
        await _start_coroutine

    from flows.flow_sys import FlowSys
    from flows.flow_tenant import FlowTenant

    worker.register_workflow(FlowSys())
    logger.info("register sys workflow")

    worker.register_workflow(FlowTenant())
    logger.info("register tenant workflow")

    from flows.flow_smolagent import FlowSmolagent

    worker.register_workflow(FlowSmolagent())
    logger.info("register smolagent workflow")

    from flows.flow_team import FlowTeam

    worker.register_workflow(FlowTeam())
    logger.info("register team workflow")

    from flows.flow_manager import FlowManager

    worker.register_workflow(FlowManager())
    logger.info("register manager workflow")

    from flows.flow_research import FlowResearch

    worker.register_workflow(FlowResearch())
    logger.info("register research workflow")

    from flows.flow_browser import FlowBrowser

    worker.register_workflow(FlowBrowser())
    logger.info("register browser workflow")

    from flows.flow_ag import FlowAg

    worker.register_workflow(FlowAg())
    logger.info("register ag workflow")

    from flows.flow_com import FlowCom

    worker.register_workflow(FlowCom())
    logger.info("register com workflow")

    from flows.flow_platform_account import FlowPlatformAccount

    worker.register_workflow(FlowPlatformAccount())
    logger.info("register com workflow")

    await worker.async_start()
