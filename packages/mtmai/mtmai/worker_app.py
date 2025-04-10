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

    # from mtmai.teams.team_social import FlowSocial

    # worker.register_workflow(FlowSocial())
    # logger.info("register social workflow")

    # from mtmai.teams.team_tooluse import FlowTooluse

    # worker.register_workflow(FlowTooluse())
    # logger.info("register tooluse workflow")

    # from mtmai.teams.team_tenant import FlowTenant

    # worker.register_workflow(FlowTenant())
    # logger.info("register tenant workflow")

    from mtmai.flows.flow_team import FlowTeam

    worker.register_workflow(FlowTeam())
    logger.info("register team workflow")

    await worker.async_start()
