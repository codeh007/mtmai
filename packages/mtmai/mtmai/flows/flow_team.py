import importlib
import os

from google.adk.agents import RunConfig
from google.adk.agents.llm_agent import Agent
from google.adk.agents.run_config import StreamingMode
from google.adk.cli.utils import envs
from google.adk.runners import Runner
from loguru import logger
from mtmai.clients.rest.models.flow_names import FlowNames
from mtmai.clients.rest.models.flow_team_input import FlowTeamInput
from mtmai.clients.tenant_client import TenantClient
from mtmai.context.context import Context
from mtmai.core.config import settings
from mtmai.mtlibs.autogen_utils.cancel_token import MtCancelToken
from mtmai.mtlibs.autogen_utils.component_loader import ComponentLoader
from mtmai.mtm_engine import mtm_engine, mtmapp

# artifact_service = InMemoryArtifactService()
from mtmai.services.artifact_service import ArticleService

artifact_service = ArticleService(
    db_url=settings.MTM_DATABASE_URL,
)
session_service = mtm_engine.get_session()
runner_dict = {}
root_agent_dict = {}


def _get_root_agent(app_name: str) -> Agent:
    """Returns the root agent for the given app."""
    if app_name in root_agent_dict:
        return root_agent_dict[app_name]
    envs.load_dotenv_for_agent(os.path.basename(app_name), settings.AGENT_DIR)
    agent_module = importlib.import_module(app_name)
    root_agent: Agent = agent_module.agent.root_agent
    root_agent_dict[app_name] = root_agent
    return root_agent


def _get_runner(app_name: str) -> Runner:
    """Returns the runner for the given app."""
    if app_name in runner_dict:
        return runner_dict[app_name]
    root_agent = _get_root_agent(app_name)
    runner = Runner(
        app_name=app_name,
        agent=root_agent,
        artifact_service=artifact_service,
        session_service=session_service,
    )
    runner_dict[app_name] = runner
    return runner


@mtmapp.workflow(
    name=FlowNames.TEAM,
    on_events=[FlowNames.TEAM],
)
class FlowTeam:
    @mtmapp.step(timeout="60m")
    async def step0(self, hatctx: Context):
        input = FlowTeamInput.from_dict(hatctx.input)

        tenant_client = TenantClient()
        session_id = input.session_id
        app_name = input.app_name
        user_id = tenant_client.tenant_id
        if app_name == "root":
            # 自动创建session
            session = session_service.get_session(
                app_name=app_name, user_id=user_id, session_id=session_id
            )
            if session:
                logger.info("Session already exists: %s", session_id)
            else:
                logger.info("New session created: %s", session_id)
                session_service.create_session(
                    app_name=app_name, user_id=user_id, state={}, session_id=session_id
                )
            if not session:
                logger.warning("Session not found: %s", session_id)
                return {"ok": False, "error": f"Session not found: {session_id}"}

            # 开始运行
            # stream_mode = StreamingMode.SSE if req.streaming else StreamingMode.NONE
            runner = _get_runner(app_name)
            async for event in runner.run_async(
                user_id=user_id,
                session_id=session_id,
                new_message=input.content.actual_instance,
                run_config=RunConfig(streaming_mode=StreamingMode.SSE),
            ):
                sse_event = event.model_dump_json(exclude_none=True, by_alias=True)
                logger.info("Generated event in agent run streaming: %s", sse_event)
                tenant_client.emit(sse_event)

            return {"ok": True}

        else:
            # 旧版 使用 autogen
            team = ComponentLoader.load_component(input.component, expected=Team)
            return await team.run(task=input, cancellation_token=MtCancelToken())
