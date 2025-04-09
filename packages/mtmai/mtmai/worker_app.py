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

    from mtmai.teams.team_social import FlowSocial

    worker.register_workflow(FlowSocial())
    logger.info("register social workflow")

    from mtmai.teams.team_tooluse import FlowTooluse

    worker.register_workflow(FlowTooluse())
    logger.info("register tooluse workflow")

    # from teams.team_social import FlowUser

    # worker.register_workflow(FlowUser())
    # logger.info("register user workflow")

    await worker.async_start()
