import logging
from datetime import timedelta

from google.genai import types  # noqa: F401
from hatchet_sdk import Context, SleepCondition
from mtmai.clients.rest.models.agent_runner_input import AgentRunnerInput
from mtmai.clients.rest.models.agent_runner_output import AgentRunnerOutput
from mtmai.core.config import settings
from mtmai.hatchet_client import hatchet
from mtmai.services.artifact_service import MtmArtifactService
from mtmai.services.gomtm_db_session_service import GomtmDatabaseSessionService

logger = logging.getLogger(__name__)


# class ShortVideoGenInput(BaseModel):
#   topic: str | None = None


# class StepOutput(BaseModel):
#   # random_number: int
#   events: list[Event]


# class RandomSum(BaseModel):
#   sum: int


agent_runner_workflow = hatchet.workflow(name="AgentRunnerWorkflow", input_validator=AgentRunnerInput)


session_service = GomtmDatabaseSessionService(
  db_url=settings.MTM_DATABASE_URL,
)

artifact_service = MtmArtifactService(
  db_url=settings.MTM_DATABASE_URL,
)


@agent_runner_workflow.task()
async def start(input: AgentRunnerInput, ctx: Context) -> AgentRunnerOutput:
  logger.info("开始执行 AgentRunnerWorkflow")
  return AgentRunnerOutput(
    content="hello1 result",
  )


@agent_runner_workflow.task(
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
