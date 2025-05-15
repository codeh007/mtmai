import logging

from hatchet_sdk import Context, EmptyModel

from ..hatchet_client import hatchet

logger = logging.getLogger(__name__)


# Declare the task to run
@hatchet.task(name="first-workflow")
def my_task(input: EmptyModel, ctx: Context) -> dict[str, int]:
    logger.info("executed task")

    return {"meaning_of_life": 42}
