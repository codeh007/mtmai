import asyncio
import importlib
import inspect
import json
import logging
import os
import pathlib
import re
import sys
import time
import traceback
import typing
from pathlib import Path
from typing import Any, List, Literal, Optional

import graphviz
from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import FileResponse, RedirectResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from fastapi.websockets import WebSocket, WebSocketDisconnect
from google.adk.agents import RunConfig
from google.adk.agents.live_request_queue import LiveRequest, LiveRequestQueue
from google.adk.agents.llm_agent import Agent
from google.adk.agents.run_config import StreamingMode
from google.adk.artifacts import BaseArtifactService
from google.adk.cli.cli_eval import EVAL_SESSION_ID_PREFIX, EvalMetric, EvalMetricResult, EvalSetResult, EvalStatus
from google.adk.cli.utils import create_empty_state, envs, evals
from google.adk.evaluation.local_eval_sets_manager import LocalEvalSetsManager
from google.adk.events.event import Event
from google.adk.runners import Runner
from google.adk.sessions import BaseSessionService
from google.adk.sessions.session import Session
from google.genai import types  # type: ignore
from mtmai.core.config import settings
from opentelemetry.sdk.trace import ReadableSpan, TracerProvider, export
from pydantic import BaseModel, ValidationError
from starlette.types import Lifespan

BASE_DIR = Path(__file__).parent.resolve()
ANGULAR_DIST_PATH = BASE_DIR / "browser"


_EVAL_SET_FILE_EXTENSION = ".evalset.json"
_EVAL_SET_RESULT_FILE_EXTENSION = ".evalset_result.json"
logger = logging.getLogger(__name__)


agents_dir = str(pathlib.Path(os.path.dirname(__file__), "..", "agents").resolve())
if agents_dir not in sys.path:
  sys.path.append(agents_dir)


def get_long_running_function_call(event: Event) -> types.FunctionCall:
  # Get the long running function call from the event
  if not event.long_running_tool_ids or not event.content or not event.content.parts:
    return
  for part in event.content.parts:
    if (
      part
      and part.function_call
      and event.long_running_tool_ids
      and part.function_call.id in event.long_running_tool_ids
    ):
      return part.function_call


def get_function_response(event: Event, function_call_id: str) -> types.FunctionResponse:
  # Get the function response for the fuction call with specified id.
  if not event.content or not event.content.parts:
    return
  for part in event.content.parts:
    if part and part.function_response and part.function_response.id == function_call_id:
      return part.function_response


class ApiServerSpanExporter(export.SpanExporter):
  def __init__(self, trace_dict):
    self.trace_dict = trace_dict

  def export(self, spans: typing.Sequence[ReadableSpan]) -> export.SpanExportResult:
    for span in spans:
      if span.name == "call_llm" or span.name == "send_data" or span.name.startswith("tool_response"):
        attributes = dict(span.attributes)
        attributes["trace_id"] = span.get_span_context().trace_id
        attributes["span_id"] = span.get_span_context().span_id
        if attributes.get("gcp.vertex.agent.event_id", None):
          self.trace_dict[attributes["gcp.vertex.agent.event_id"]] = attributes
    return export.SpanExportResult.SUCCESS

  def force_flush(self, timeout_millis: int = 30000) -> bool:
    return True


class AgentRunRequest(BaseModel):
  app_name: str
  user_id: str
  session_id: str
  new_message: types.Content
  streaming: bool = False


class AddSessionToEvalSetRequest(BaseModel):
  eval_id: str
  session_id: str
  user_id: str


class RunEvalRequest(BaseModel):
  eval_ids: list[str]  # if empty, then all evals in the eval set are run.
  eval_metrics: list[EvalMetric]


class RunEvalResult(BaseModel):
  eval_set_id: str
  eval_id: str
  final_eval_status: EvalStatus
  eval_metric_results: list[tuple[EvalMetric, EvalMetricResult]]
  session_id: str


default_agents_dir = str(Path(os.path.dirname(__file__), "..", "agents").resolve())


def configure_adk_web_api(
  *,
  app: FastAPI,
  session_service: BaseSessionService,
  artifact_service: BaseArtifactService,
  agent_dir: str = default_agents_dir,
  # session_db_url: str = "",
  web: bool = True,
  # trace_to_cloud: bool = False,
  lifespan: Optional[Lifespan[FastAPI]] = None,
) -> FastAPI:
  # InMemory tracing dict.
  trace_dict: dict[str, Any] = {}

  # # Set up tracing in the FastAPI server.
  provider = TracerProvider()
  provider.add_span_processor(export.SimpleSpanProcessor(ApiServerSpanExporter(trace_dict)))
  eval_sets_manager = LocalEvalSetsManager(agent_dir=agent_dir)
  runner_dict = {}
  root_agent_dict = {}
  agent_engine_id = ""
  exit_stacks = []

  @app.get("/list-apps")
  def list_apps() -> list[str]:
    base_path = Path.cwd() / agent_dir
    if not base_path.exists():
      raise HTTPException(status_code=404, detail="Path not found")
    if not base_path.is_dir():
      raise HTTPException(status_code=400, detail="Not a directory")
    agent_names = [
      x
      for x in os.listdir(base_path)
      if os.path.isdir(os.path.join(base_path, x)) and not x.startswith(".") and x != "__pycache__"
    ]
    agent_names.sort()
    return agent_names

  @app.get("/debug/trace/{event_id}")
  async def get_trace_dict(event_id: str) -> Any:
    event_dict = trace_dict.get(event_id, None)
    if event_dict is None:
      raise HTTPException(status_code=404, detail="Trace not found")
    return event_dict

  @app.get(
    "/apps/{app_name}/users/{user_id}/sessions/{session_id}",
    response_model_exclude_none=True,
  )
  async def get_session(app_name: str, user_id: str, session_id: str) -> Session:
    # Connect to managed session if agent_engine_id is set.
    app_name = agent_engine_id if agent_engine_id else app_name
    session = await session_service.get_session(app_name=app_name, user_id=user_id, session_id=session_id)
    if not session:
      raise HTTPException(status_code=404, detail="Session not found")
    return session

  @app.get(
    "/apps/{app_name}/users/{user_id}/sessions",
    response_model_exclude_none=True,
  )
  async def list_sessions(app_name: str, user_id: str) -> list[Session]:
    # Connect to managed session if agent_engine_id is set.
    app_name = agent_engine_id if agent_engine_id else app_name
    return [
      session
      for session in await session_service.list_sessions(app_name=app_name, user_id=user_id).sessions
      # Remove sessions that were generated as a part of Eval.
      if not session.id.startswith(EVAL_SESSION_ID_PREFIX)
    ]

  @app.post(
    "/apps/{app_name}/users/{user_id}/sessions/{session_id}",
    response_model_exclude_none=True,
  )
  def create_session_with_id(
    app_name: str,
    user_id: str,
    session_id: str,
    state: Optional[dict[str, Any]] = None,
  ) -> Session:
    # Connect to managed session if agent_engine_id is set.
    app_name = agent_engine_id if agent_engine_id else app_name
    if session_service.get_session(app_name=app_name, user_id=user_id, session_id=session_id) is not None:
      logger.warning("Session already exists: %s", session_id)
      raise HTTPException(status_code=400, detail=f"Session already exists: {session_id}")

    logger.info(f"New session created: {session_id}, user_id: {user_id}")
    return session_service.create_session(app_name=app_name, user_id=user_id, state=state, session_id=session_id)

  @app.post(
    "/apps/{app_name}/users/{user_id}/sessions",
    response_model_exclude_none=True,
  )
  def create_session(
    app_name: str,
    user_id: str,
    state: Optional[dict[str, Any]] = None,
  ) -> Session:
    # Connect to managed session if agent_engine_id is set.
    app_name = agent_engine_id if agent_engine_id else app_name

    logger.info("New session created")
    return session_service.create_session(app_name=app_name, user_id=user_id, state=state)

  def _get_eval_set_file_path(app_name, agent_dir, eval_set_id) -> str:
    return os.path.join(
      agent_dir,
      app_name,
      eval_set_id + _EVAL_SET_FILE_EXTENSION,
    )

  @app.post(
    "/apps/{app_name}/eval_sets/{eval_set_id}",
    response_model_exclude_none=True,
  )
  def create_eval_set(
    app_name: str,
    eval_set_id: str,
  ):
    """Creates an eval set, given the id."""
    pattern = r"^[a-zA-Z0-9_]+$"
    if not bool(re.fullmatch(pattern, eval_set_id)):
      raise HTTPException(
        status_code=400,
        detail=(f"Invalid eval set id. Eval set id should have the `{pattern}`" " format"),
      )
    # Define the file path
    new_eval_set_path = _get_eval_set_file_path(app_name, agent_dir, eval_set_id)

    logger.info("Creating eval set file `%s`", new_eval_set_path)

    if not os.path.exists(new_eval_set_path):
      # Write the JSON string to the file
      logger.info("Eval set file doesn't exist, we will create a new one.")
      with open(new_eval_set_path, "w") as f:
        empty_content = json.dumps([], indent=2)
        f.write(empty_content)

  @app.get(
    "/apps/{app_name}/eval_sets",
    response_model_exclude_none=True,
  )
  def list_eval_sets(app_name: str) -> list[str]:
    """Lists all eval sets for the given app."""
    eval_set_file_path = os.path.join(agent_dir, app_name)
    eval_sets = []
    for file in os.listdir(eval_set_file_path):
      if file.endswith(_EVAL_SET_FILE_EXTENSION):
        eval_sets.append(os.path.basename(file).removesuffix(_EVAL_SET_FILE_EXTENSION))

    return sorted(eval_sets)

  @app.post(
    "/apps/{app_name}/eval_sets/{eval_set_id}/add_session",
    response_model_exclude_none=True,
  )
  def add_session_to_eval_set(app_name: str, eval_set_id: str, req: AddSessionToEvalSetRequest):
    pattern = r"^[a-zA-Z0-9_]+$"
    if not bool(re.fullmatch(pattern, req.eval_id)):
      raise HTTPException(
        status_code=400,
        detail=f"Invalid eval id. Eval id should have the `{pattern}` format",
      )

    # Get the session
    session = session_service.get_session(app_name=app_name, user_id=req.user_id, session_id=req.session_id)
    assert session, "Session not found."
    # Load the eval set file data
    eval_set_file_path = _get_eval_set_file_path(app_name, agent_dir, eval_set_id)
    with open(eval_set_file_path, "r") as file:
      eval_set_data = json.load(file)  # Load JSON into a list

    if [x for x in eval_set_data if x["name"] == req.eval_id]:
      raise HTTPException(
        status_code=400,
        detail=(f"Eval id `{req.eval_id}` already exists in `{eval_set_id}`" " eval set."),
      )

    # Convert the session data to evaluation format
    test_data = evals.convert_session_to_eval_format(session)

    # Populate the session with initial session state.
    initial_session_state = create_empty_state(_get_root_agent(app_name))

    eval_set_data.append(
      {
        "name": req.eval_id,
        "data": test_data,
        "initial_session": {
          "state": initial_session_state,
          "app_name": app_name,
          "user_id": req.user_id,
        },
      }
    )
    # Serialize the test data to JSON and write to the eval set file.
    with open(eval_set_file_path, "w") as f:
      f.write(json.dumps(eval_set_data, indent=2))

  @app.get(
    "/apps/{app_name}/eval_sets/{eval_set_id}/evals",
    response_model_exclude_none=True,
  )
  def list_evals_in_eval_set(
    app_name: str,
    eval_set_id: str,
  ) -> list[str]:
    """Lists all evals in an eval set."""
    # Load the eval set file data
    eval_set_file_path = _get_eval_set_file_path(app_name, agent_dir, eval_set_id)
    with open(eval_set_file_path, "r") as file:
      eval_set_data = json.load(file)  # Load JSON into a list

    return sorted([x["name"] for x in eval_set_data])

  @app.post(
    "/apps/{app_name}/eval_sets/{eval_set_id}/run_eval",
    response_model_exclude_none=True,
  )
  async def run_eval(app_name: str, eval_set_id: str, req: RunEvalRequest) -> list[RunEvalResult]:
    """Runs an eval given the details in the eval request."""
    from google.adk.cli.cli_eval import run_evals

    # Create a mapping from eval set file to all the evals that needed to be
    # run.
    envs.load_dotenv_for_agent(os.path.basename(app_name), agent_dir)

    eval_set = eval_sets_manager.get_eval_set(app_name, eval_set_id)

    if req.eval_ids:
      eval_cases = [e for e in eval_set.eval_cases if e.eval_id in req.eval_ids]
      eval_set_to_evals = {eval_set_id: eval_cases}
    else:
      logger.info("Eval ids to run list is empty. We will run all eval cases.")
      eval_set_to_evals = {eval_set_id: eval_set.eval_cases}

    root_agent = await _get_root_agent_async(app_name)
    run_eval_results = []
    eval_case_results = []
    async for eval_case_result in run_evals(
      eval_set_to_evals,
      root_agent,
      getattr(root_agent, "reset_data", None),
      req.eval_metrics,
      session_service=session_service,
      artifact_service=artifact_service,
    ):
      run_eval_results.append(
        RunEvalResult(
          app_name=app_name,
          eval_set_file=eval_case_result.eval_set_file,
          eval_set_id=eval_set_id,
          eval_id=eval_case_result.eval_id,
          final_eval_status=eval_case_result.final_eval_status,
          eval_metric_results=eval_case_result.eval_metric_results,
          overall_eval_metric_results=eval_case_result.overall_eval_metric_results,
          eval_metric_result_per_invocation=eval_case_result.eval_metric_result_per_invocation,
          user_id=eval_case_result.user_id,
          session_id=eval_case_result.session_id,
        )
      )
      eval_case_result.session_details = session_service.get_session(
        app_name=app_name,
        user_id=eval_case_result.user_id,
        session_id=eval_case_result.session_id,
      )
      eval_case_results.append(eval_case_result)

    timestamp = time.time()
    eval_set_result_name = app_name + "_" + eval_set_id + "_" + str(timestamp)
    eval_set_result = EvalSetResult(
      eval_set_result_id=eval_set_result_name,
      eval_set_result_name=eval_set_result_name,
      eval_set_id=eval_set_id,
      eval_case_results=eval_case_results,
      creation_timestamp=timestamp,
    )

    # Write eval result file, with eval_set_result_name.
    app_eval_history_dir = os.path.join(agent_dir, app_name, ".adk", "eval_history")
    if not os.path.exists(app_eval_history_dir):
      os.makedirs(app_eval_history_dir)
    # Convert to json and write to file.
    eval_set_result_json = eval_set_result.model_dump_json()
    eval_set_result_file_path = os.path.join(
      app_eval_history_dir,
      eval_set_result_name + _EVAL_SET_RESULT_FILE_EXTENSION,
    )
    logger.info("Writing eval result to file: %s", eval_set_result_file_path)
    with open(eval_set_result_file_path, "w") as f:
      f.write(json.dumps(eval_set_result_json, indent=2))

    return run_eval_results

  @app.delete("/apps/{app_name}/users/{user_id}/sessions/{session_id}")
  def delete_session(app_name: str, user_id: str, session_id: str):
    # Connect to managed session if agent_engine_id is set.
    app_name = agent_engine_id if agent_engine_id else app_name
    session_service.delete_session(app_name=app_name, user_id=user_id, session_id=session_id)

  @app.get(
    "/apps/{app_name}/users/{user_id}/sessions/{session_id}/artifacts/{artifact_name}",
    response_model_exclude_none=True,
  )
  def load_artifact(
    app_name: str,
    user_id: str,
    session_id: str,
    artifact_name: str,
    version: Optional[int] = Query(None),
  ) -> Optional[types.Part]:
    app_name = agent_engine_id if agent_engine_id else app_name
    artifact = artifact_service.load_artifact(
      app_name=app_name,
      user_id=user_id,
      session_id=session_id,
      filename=artifact_name,
      version=version,
    )
    if not artifact:
      raise HTTPException(status_code=404, detail="Artifact not found")
    return artifact

  @app.get(
    "/apps/{app_name}/users/{user_id}/sessions/{session_id}/artifacts/{artifact_name}/versions/{version_id}",
    response_model_exclude_none=True,
  )
  def load_artifact_version(
    app_name: str,
    user_id: str,
    session_id: str,
    artifact_name: str,
    version_id: int,
  ) -> Optional[types.Part]:
    app_name = agent_engine_id if agent_engine_id else app_name
    artifact = artifact_service.load_artifact(
      app_name=app_name,
      user_id=user_id,
      session_id=session_id,
      filename=artifact_name,
      version=version_id,
    )
    if not artifact:
      raise HTTPException(status_code=404, detail="Artifact not found")
    return artifact

  @app.get(
    "/apps/{app_name}/users/{user_id}/sessions/{session_id}/artifacts",
    response_model_exclude_none=True,
  )
  def list_artifact_names(app_name: str, user_id: str, session_id: str) -> list[str]:
    app_name = agent_engine_id if agent_engine_id else app_name
    return artifact_service.list_artifact_keys(app_name=app_name, user_id=user_id, session_id=session_id)

  @app.get(
    "/apps/{app_name}/users/{user_id}/sessions/{session_id}/artifacts/{artifact_name}/versions",
    response_model_exclude_none=True,
  )
  def list_artifact_versions(app_name: str, user_id: str, session_id: str, artifact_name: str) -> list[int]:
    app_name = agent_engine_id if agent_engine_id else app_name
    return artifact_service.list_versions(
      app_name=app_name,
      user_id=user_id,
      session_id=session_id,
      filename=artifact_name,
    )

  @app.delete(
    "/apps/{app_name}/users/{user_id}/sessions/{session_id}/artifacts/{artifact_name}",
  )
  def delete_artifact(app_name: str, user_id: str, session_id: str, artifact_name: str):
    app_name = agent_engine_id if agent_engine_id else app_name
    artifact_service.delete_artifact(
      app_name=app_name,
      user_id=user_id,
      session_id=session_id,
      filename=artifact_name,
    )

  @app.post("/run", response_model_exclude_none=True)
  async def agent_run(req: AgentRunRequest) -> list[Event]:
    # Connect to managed session if agent_engine_id is set.
    app_id = agent_engine_id if agent_engine_id else req.app_name
    session = session_service.get_session(app_name=app_id, user_id=req.user_id, session_id=req.session_id)
    if not session:
      raise HTTPException(status_code=404, detail="Session not found")
    runner = _get_runner(req.app_name)
    events = [
      event
      async for event in runner.run_async(
        user_id=req.user_id,
        session_id=req.session_id,
        new_message=req.new_message,
      )
    ]
    logger.info("Generated %s events in agent run: %s", len(events), events)
    return events

  @app.post("/run_sse")
  async def agent_run_sse(req: AgentRunRequest) -> StreamingResponse:
    # Connect to managed session if agent_engine_id is set.
    app_id = agent_engine_id if agent_engine_id else req.app_name
    user_id = settings.DEMO_USER_ID
    # SSE endpoint
    session = session_service.get_session(app_name=app_id, user_id=user_id, session_id=req.session_id)

    # 新增代码
    if not session:
      logger.info(f"New session created: {req.session_id}")
      session = session_service.create_session(
        app_name=app_id,
        user_id=user_id,
        state={},
        session_id=req.session_id,
      )
    if not session:
      raise HTTPException(status_code=404, detail="Session not found")

    # Convert the events to properly formatted SSE
    async def event_generator():
      try:
        stream_mode = StreamingMode.SSE if req.streaming else StreamingMode.NONE
        runner = _get_runner(req.app_name)

        # 新增:
        long_running_function_call, long_running_function_response, ticket_id = None, None, None

        events = runner.run_async(
          user_id=user_id,
          session_id=req.session_id,
          new_message=req.new_message,
          run_config=RunConfig(streaming_mode=stream_mode),
        )
        events_async = runner.run_async(session_id=session.id, user_id=user_id, new_message=req.new_message)
        async for event in events_async:
          if not long_running_function_call:
            long_running_function_call = get_long_running_function_call(event)
          else:
            long_running_function_response = get_function_response(event, long_running_function_call.id)
          if long_running_function_response:
            ticket_id = long_running_function_response.response["ticket_id"]
          # Format as SSE data
          sse_event = event.model_dump_json(exclude_none=True, by_alias=True)
          logger.info(f"Generated event in agent run streaming: {sse_event}")
          yield f"data: {sse_event}\n\n"

        # 如果收到人类确认信号(长时任务)
        if long_running_function_response:
          # query the status of the correpsonding ticket via tciket_id
          # send back an intermediate / final response
          updated_response = long_running_function_response.model_copy(deep=True)
          updated_response.response = {"status": "approved"}
          async for event in runner.run_async(
            session_id=session.id,
            user_id=user_id,
            new_message=types.Content(parts=[types.Part(function_response=updated_response)], role="user"),
          ):
            if event.content and event.content.parts:
              if text := "".join(part.text or "" for part in event.content.parts):
                logger.info(f"[{event.author}]: {text}")

      except Exception as e:
        logger.exception(e)
        # You might want to yield an error event here
        yield f'data: {{"error": "{str(e)}"}}\n\n'

    # Returns a streaming response with the proper media type for SSE
    return StreamingResponse(
      event_generator(),
      media_type="text/event-stream",
    )

  @app.get(
    "/apps/{app_name}/users/{user_id}/sessions/{session_id}/events/{event_id}/graph",
    response_model_exclude_none=True,
  )
  def get_event_graph(app_name: str, user_id: str, session_id: str, event_id: str):
    # Connect to managed session if agent_engine_id is set.
    app_id = agent_engine_id if agent_engine_id else app_name
    session = session_service.get_session(app_name=app_id, user_id=user_id, session_id=session_id)
    session_events = session.events if session else []
    event = next((x for x in session_events if x.id == event_id), None)
    if not event:
      return {}

    from google.adk.cli import agent_graph

    function_calls = event.get_function_calls()
    function_responses = event.get_function_responses()
    root_agent = _get_root_agent(app_name)
    dot_graph = None
    if function_calls:
      function_call_highlights = []
      for function_call in function_calls:
        from_name = event.author
        to_name = function_call.name
        function_call_highlights.append((from_name, to_name))
        dot_graph = agent_graph.get_agent_graph(root_agent, function_call_highlights)
    elif function_responses:
      function_responses_highlights = []
      for function_response in function_responses:
        from_name = function_response.name
        to_name = event.author
        function_responses_highlights.append((from_name, to_name))
        dot_graph = agent_graph.get_agent_graph(root_agent, function_responses_highlights)
    else:
      from_name = event.author
      to_name = ""
      dot_graph = agent_graph.get_agent_graph(root_agent, [(from_name, to_name)])
    if dot_graph and isinstance(dot_graph, graphviz.Digraph):
      return {"dot_src": dot_graph.source}
    else:
      return {}

  @app.websocket("/run_live")
  async def agent_live_run(
    websocket: WebSocket,
    app_name: str,
    user_id: str,
    session_id: str,
    modalities: List[Literal["TEXT", "AUDIO"]] = Query(default=["TEXT", "AUDIO"]),  # Only allows "TEXT" or "AUDIO"
  ) -> None:
    await websocket.accept()

    # Connect to managed session if agent_engine_id is set.
    app_id = agent_engine_id if agent_engine_id else app_name
    session = session_service.get_session(app_name=app_id, user_id=user_id, session_id=session_id)
    if not session:
      # Accept first so that the client is aware of connection establishment,
      # then close with a specific code.
      await websocket.close(code=1002, reason="Session not found")
      return

    live_request_queue = LiveRequestQueue()

    async def forward_events():
      runner = _get_runner(app_name)
      async for event in runner.run_live(session=session, live_request_queue=live_request_queue):
        await websocket.send_text(event.model_dump_json(exclude_none=True, by_alias=True))

    async def process_messages():
      try:
        while True:
          data = await websocket.receive_text()
          # Validate and send the received message to the live queue.
          live_request_queue.send(LiveRequest.model_validate_json(data))
      except ValidationError as ve:
        logger.error("Validation error in process_messages: %s", ve)

    # Run both tasks concurrently and cancel all if one fails.
    tasks = [
      asyncio.create_task(forward_events()),
      asyncio.create_task(process_messages()),
    ]
    done, pending = await asyncio.wait(tasks, return_when=asyncio.FIRST_EXCEPTION)
    try:
      # This will re-raise any exception from the completed tasks.
      for task in done:
        task.result()
    except WebSocketDisconnect:
      logger.info("Client disconnected during process_messages.")
    except Exception as e:
      logger.exception("Error during live websocket communication: %s", e)
      traceback.print_exc()
    finally:
      for task in pending:
        task.cancel()

  def _get_root_agent(app_name: str) -> Agent:
    """Returns the root agent for the given app."""
    if app_name in root_agent_dict:
      return root_agent_dict[app_name]
    envs.load_dotenv_for_agent(os.path.basename(app_name), agent_dir)
    agent_module = importlib.import_module(app_name)
    root_agent: Agent = agent_module.agent.root_agent
    root_agent_dict[app_name] = root_agent
    return root_agent

  async def _get_root_agent_async(app_name: str) -> Agent:
    """Returns the root agent for the given app."""
    if app_name in root_agent_dict:
      return root_agent_dict[app_name]
    agent_module = importlib.import_module(app_name)
    if getattr(agent_module.agent, "root_agent"):
      root_agent = agent_module.agent.root_agent
    else:
      raise ValueError(f'Unable to find "root_agent" from {app_name}.')

    # Handle an awaitable root agent and await for the actual agent.
    if inspect.isawaitable(root_agent):
      try:
        agent, exit_stack = await root_agent
        exit_stacks.append(exit_stack)
        root_agent = agent
      except Exception as e:
        raise RuntimeError(f"error getting root agent, {e}") from e

    root_agent_dict[app_name] = root_agent
    return root_agent

  def _get_runner(app_name: str) -> Runner:
    """Returns the runner for the given app."""
    if app_name in runner_dict:
      return runner_dict[app_name]
    root_agent = _get_root_agent(app_name)
    runner = Runner(
      app_name=agent_engine_id if agent_engine_id else app_name,
      agent=root_agent,
      artifact_service=artifact_service,
      session_service=session_service,
    )
    runner_dict[app_name] = runner
    return runner

  if web:
    BASE_DIR = Path(__file__).parent.resolve()
    ANGULAR_DIST_PATH = BASE_DIR / "browser"

    @app.get("/")
    async def redirect_to_dev_ui():
      return RedirectResponse("/dev-ui")

    @app.get("/dev-ui")
    async def dev_ui():
      return FileResponse(BASE_DIR / "browser/index.html")

    app.mount("/", StaticFiles(directory=ANGULAR_DIST_PATH, html=True), name="static")
  return app
