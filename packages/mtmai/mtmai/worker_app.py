async def run_worker():
    try:
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

        # from mtmai.flows.flow_tiktok import FlowTiktok

        # worker.register_workflow(FlowTiktok())
        # logger.info("register tiktok workflow")

        await worker.async_start()
    except Exception as e:
        logger.error(f"worker error: {e}")

        raise e
