import logging
from datetime import timedelta

from google.adk.agents import RunConfig
from google.adk.agents.run_config import StreamingMode
from google.adk.events.event import Event
from google.adk.runners import Runner
from google.genai import types  # noqa: F401
from hatchet_sdk import Context, SleepCondition
from mtmai.agents.shortvideo_agent.shortvideo_agent import new_shortvideo_agent
from mtmai.core.config import settings
from mtmai.hatchet_client import hatchet
from mtmai.mtlibs.id import generate_uuid
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


short_video_gen_workflow = hatchet.workflow(name="ShortVideoGenWorkflow2", input_validator=ShortVideoGenInput)


session_service = GomtmDatabaseSessionService(
  db_url=settings.MTM_DATABASE_URL,
)

artifact_service = MtmArtifactService(
  db_url=settings.MTM_DATABASE_URL,
)


@short_video_gen_workflow.task()
async def start(input: ShortVideoGenInput, ctx: Context) -> StepOutput:
  """
  开始生成 topic
  """

  logger.info("开始生成 topic")
  session_id = generate_uuid()
  adk_app_name = "shortvideo_agent"
  session = await session_service.get_session(
    app_name=adk_app_name,
    user_id=settings.DEMO_USER_ID,
    session_id=session_id,
  )
  if not session:
    logger.info(f"New session created: {session_id}")
    session = session_service.create_session(
      app_name=adk_app_name,
      user_id=settings.DEMO_USER_ID,
      state={},
      session_id=session_id,
    )
  if not session:
    raise Exception("session not found")
  agent = new_shortvideo_agent()

  runner = Runner(
    app_name=adk_app_name,
    agent=agent,
    artifact_service=artifact_service,
    session_service=session_service,
  )
  events = []
  async for event in runner.run_async(
    user_id=settings.DEMO_USER_ID,
    session_id=session_id,
    new_message=types.Content(
      role="user",
      parts=[types.Part(text=input.topic)],
    ),
    run_config=RunConfig(streaming_mode=StreamingMode.SSE),
  ):
    events.append(event)
    logger.info(event)
    if event.is_final_response():
      return {"events": events}

  return {"events": events}


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
