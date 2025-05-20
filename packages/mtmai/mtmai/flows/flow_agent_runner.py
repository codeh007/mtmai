import logging
from datetime import timedelta

from google.adk.events.event import Event
from google.genai import types  # noqa: F401
from hatchet_sdk import Context, SleepCondition
from mtmai.core.config import settings
from mtmai.hatchet_client import hatchet
from mtmai.services.artifact_service import MtmArtifactService
from mtmai.services.gomtm_db_session_service import GomtmDatabaseSessionService
from pydantic import BaseModel

logger = logging.getLogger(__name__)


class ShortVideoGenInput(BaseModel):
  topic: str | None = None


class StepOutput(BaseModel):
  # random_number: int
  events: list[Event]


class RandomSum(BaseModel):
  sum: int


short_video_gen_workflow = hatchet.workflow(name="AgentRunnerWorkflow", input_validator=ShortVideoGenInput)


session_service = GomtmDatabaseSessionService(
  db_url=settings.MTM_DATABASE_URL,
)

artifact_service = MtmArtifactService(
  db_url=settings.MTM_DATABASE_URL,
)


@short_video_gen_workflow.task()
async def start(input: ShortVideoGenInput, ctx: Context) -> StepOutput:
  """ """

  logger.info("开始执行 AgentRunnerWorkflow")

  return {"events": "hello1"}


@short_video_gen_workflow.task(
  parents=[start],
  wait_for=[
    SleepCondition(
      timedelta(seconds=1),
    )
  ],
)
async def wait_for_sleep(input, ctx: Context) -> dict:
  logger.info("到达 wait_for_sleep")
  return {"步骤2": input}
