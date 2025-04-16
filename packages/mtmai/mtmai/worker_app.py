async def run_worker():
    from loguru import logger

    from mtmai.core.config import settings
    from mtmai.mtm_engine import mtmapp

    logger.info("booting worker")
    await mtmapp.boot()

    from mtmai.otel import setup_instrument

    setup_instrument()

    worker = mtmapp.worker(settings.WORKER_NAME)

    from mtmai.flows.flow_team import FlowTeam

    worker.register_workflow(FlowTeam())
    logger.info("register team workflow")

    await worker.async_start()
