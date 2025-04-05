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

    from mtmai.flows.flow_tenant import FlowTenant

    worker.register_workflow(FlowTenant())
    logger.info("register tenant workflow")

    from mtmai.flows.flow_smolagent import FlowSmolagent

    worker.register_workflow(FlowSmolagent())
    logger.info("register smolagent workflow")

    from mtmai.flows.flow_ag import FlowAg

    worker.register_workflow(FlowAg())
    logger.info("register ag workflow")

    from mtmai.flows.flow_resource import FlowResource

    worker.register_workflow(FlowResource())
    logger.info("register FlowResource")

    await worker.async_start()
