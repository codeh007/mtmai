import importlib
import os
import pathlib
import sys

import httpx
from fastapi import APIRouter, HTTPException, Request
from fastapi.encoders import jsonable_encoder
from fastapi.responses import StreamingResponse
from google.adk.agents import RunConfig
from google.adk.agents.llm_agent import Agent
from google.adk.agents.run_config import StreamingMode
from google.adk.artifacts import InMemoryArtifactService
from google.adk.cli.utils import envs
from google.adk.runners import Runner
from google.genai import types
from loguru import logger
from pydantic import BaseModel
from smolagents import ActionStep, CodeAgent

from mtmai.clients.rest.models.agent_run_request_v3 import AgentRunRequestV3
from mtmai.core.config import settings
from mtmai.model_client.utils import get_default_smolagents_model
from mtmai.services.gomtm_db_session_service import GomtmDatabaseSessionService

agents_dir = str(pathlib.Path(os.path.dirname(__file__), "..", "agents").resolve())
if agents_dir not in sys.path:
    sys.path.append(agents_dir)
router = APIRouter()
runner_dict = {}
root_agent_dict = {}
agent_engine_id = ""

# session_service = InMemorySessionService()
session_service = GomtmDatabaseSessionService(settings.MTM_DATABASE_URL)
artifact_service = InMemoryArtifactService()


class SmolAgentRequest(BaseModel):
    app_name: str
    prompt: str
    session_id: str | None = None


class AgentRunRequest(BaseModel):
    app_name: str | None = None
    user_id: str | None = None
    session_id: str | None = None
    new_message: types.Content | str | None = None
    streaming: bool = False


async def get_agent_state(agent_name: str, session_id: str):
    url = f"{settings.WORKER_GATEWAY_URL}/agents/{agent_name}/{session_id}/state"
    response = httpx.get(
        url,
        # headers={"Content-Type": "application/json"},
        # json={"session_id": session_id},
    )
    agent_state = response.json()
    return agent_state


def _get_root_agent(app_name: str) -> Agent:
    """Returns the root agent for the given app."""
    if app_name in root_agent_dict:
        return root_agent_dict[app_name]
    envs.load_dotenv_for_agent(os.path.basename(app_name), str(agents_dir))
    agent_module = importlib.import_module(app_name)
    root_agent: Agent = agent_module.agent.root_agent
    root_agent_dict[app_name] = root_agent
    return root_agent


def _get_runner(app_name: str) -> Runner:
    """Returns the runner for the given app."""
    if app_name in runner_dict:
        return runner_dict[app_name]
    root_agent = _get_root_agent(app_name)
    # from mtmai.agents import root_agent

    # root_agent = agent_engines.get_agent(agent_engine_id)
    runner = Runner(
        app_name=agent_engine_id if agent_engine_id else app_name,
        agent=root_agent,
        artifact_service=artifact_service,
        session_service=session_service,
    )
    runner_dict[app_name] = runner
    return runner


@router.post("/smolagent", include_in_schema=False)
async def smolagent(req: SmolAgentRequest):
    def step_callback(step_context):
        if isinstance(step_context, ActionStep):
            logger.info(step_context)
            if req.session_id:
                logger.info(f"session_id: {req.session_id}")

                step_cb_url = f"{settings.WORKER_GATEWAY_URL}/agents/step_cb"
                try:
                    # async with httpx.AsyncClient() as client:
                    response = httpx.post(
                        step_cb_url,
                        headers={"Content-Type": "application/json"},
                        json={
                            "session_id": req.session_id,
                            "data": jsonable_encoder(step_context),
                        },
                    )
                    logger.info(
                        f"step_cb_url: {step_cb_url} response: {response.json()}"
                    )
                except Exception as e:
                    logger.error(f"step_cb_url: {step_cb_url} error: {e}")

        else:
            logger.info(f"其他步骤: {step_context}")

    agent_state = await get_agent_state("Chat", req.session_id)
    agent = CodeAgent(
        model=get_default_smolagents_model(),
        tools=[],
        max_steps=20,
        verbosity_level=2,
        step_callbacks=[step_callback],
    )
    result = agent.run(req.prompt)
    # return {"status": "ok", "agent_output": result}

    # Convert the events to properly formatted SSE
    async def event_generator():
        try:
            stream_mode = StreamingMode.SSE if req.streaming else StreamingMode.NONE
            runner = _get_runner(req.app_name)
            async for event in runner.run_async(
                user_id=req.user_id,
                session_id=req.session_id,
                new_message=req.new_message,
                run_config=RunConfig(streaming_mode=stream_mode),
            ):
                # Format as SSE data
                sse_event = event.model_dump_json(exclude_none=True, by_alias=True)
                logger.info("Generated event in agent run streaming: %s", sse_event)
                yield f"data: {sse_event}\n\n"
        except Exception as e:
            logger.exception("Error in event_generator: %s", e)
            # You might want to yield an error event here
            yield f'data: {{"error": "{str(e)}"}}\n\n'

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
    )


@router.post("/run_sse_v3")
async def agent_run_sse_v3(request: Request) -> StreamingResponse:
    body = await request.json()
    req = AgentRunRequestV3.from_dict(body)

    # Connect to managed session if agent_engine_id is set.
    # app_id = req.app_name
    # SSE endpoint
    session = session_service.get_session(
        app_name=req.app_name,
        user_id=req.user_id,
        session_id=req.session_id,
    )

    # 新增代码
    if not session:
        logger.info("New session created: %s", req.session_id)
        session = session_service.create_session(
            app_name=req.app_name,
            user_id=req.user_id,
            state=req.init_state,
            session_id=req.session_id,
        )
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    # Convert the events to properly formatted SSE
    async def event_generator():
        content = types.Content.model_validate(req.new_message)
        try:
            stream_mode = StreamingMode.SSE if req.streaming else StreamingMode.NONE
            runner = _get_runner(req.app_name)
            async for event in runner.run_async(
                user_id=req.user_id,
                session_id=req.session_id,
                new_message=content,
                run_config=RunConfig(streaming_mode=stream_mode),
            ):
                # Format as SSE data
                sse_event = event.model_dump_json(exclude_none=True, by_alias=True)
                logger.info("Generated event in agent run streaming: %s", sse_event)
                yield f"data: {sse_event}\n\n"
        except Exception as e:
            logger.exception("Error in event_generator: %s", e)
            # You might want to yield an error event here
            yield f'data: {{"error": "{str(e)}"}}\n\n'

    # Returns a streaming response with the proper media type for SSE
    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
    )
