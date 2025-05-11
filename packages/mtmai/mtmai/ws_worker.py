import asyncio
import importlib
import json
import os
import random
import sys
import traceback
from pathlib import Path

from google.adk.agents.live_request_queue import LiveRequest, LiveRequestQueue
from google.adk.agents.llm_agent import Agent
from google.adk.cli.utils import envs
from google.adk.runners import Runner
from loguru import logger
from pydantic import ValidationError
from websockets.sync.client import Connection, connect

from mtmai.core.config import settings
from mtmai.mtlibs.utils import http_url_ws
from mtmai.services.artifact_service import ArticleService
from mtmai.services.gomtm_db_session_service import GomtmDatabaseSessionService

default_agents_dir = str(Path(os.path.dirname(__file__), "..", "agents").resolve())
if default_agents_dir not in sys.path:
    sys.path.append(default_agents_dir)

artifact_service = ArticleService(
    db_url=settings.MTM_DATABASE_URL,
)
session_service = GomtmDatabaseSessionService(
    db_url=settings.MTM_DATABASE_URL,
)
runner_dict = {}
root_agent_dict = {}


def _get_root_agent(app_name: str) -> Agent:
    """Returns the root agent for the given app."""
    if app_name in root_agent_dict:
        return root_agent_dict[app_name]
    envs.load_dotenv_for_agent(os.path.basename(app_name), default_agents_dir)
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


class WSAgentWorker:
    """基于 web socket 的worker"""

    def __init__(self):
        self.ws_client = None
        self.worker_id = random.randint(1000000000000000000, 9999999999999999999)

    async def start(self):
        await self.connect()

    async def connect(self):
        ws_url = f"{http_url_ws(settings.WORKER_GATEWAY_URL)}/api/worker-agent/default"
        logger.info(f"连接到 {ws_url}")
        max_retry = 10
        retry_interval = 5
        retry_count = 0

        while retry_count < max_retry:
            try:
                with connect(ws_url) as websocket:
                    retry_count = 0  # 重置重试计数
                    while True:
                        try:
                            message_data = websocket.recv()
                            msg = json.loads(message_data)
                            msg_type = msg["type"]
                            if msg_type == "log":
                                pass
                            elif msg_type == "cf_agent_state":
                                logger.info(msg)
                            elif msg_type == "call_adk_agent":
                                await self.on_call_agent(websocket, msg)
                            elif msg_type == "connected":
                                await self.on_connected(websocket, msg)
                            else:
                                logger.error(f"未知的消息类型: {msg_type}")
                        except Exception as e:
                            traceback.print_exc()
                            logger.error(f"处理消息时出错: {e}")
                            break

            except Exception as e:
                retry_count += 1
                logger.error(f"WebSocket连接失败 (尝试 {retry_count}/{max_retry}): {e}")
                if retry_count < max_retry:
                    import time

                    time.sleep(retry_interval)
                else:
                    logger.error("达到最大重试次数,退出重连")
                    break

    def on_connected(self, ws, msg):
        logger.info("WebSocket连接成功")
        ws.send(json.dumps({"type": "worker_init", "worker_id": self.worker_id}))

    def log(self, msg):
        logger.info(f"收到来自服务端的事件: {msg}")

    async def on_call_agent(self, ws: Connection, msg):
        logger.info(f"收到来自服务端的调用请求: {msg}")
        agent_name = msg.get("agent_name", "shortvideo_agent")
        user_id = msg.get("user_id", "default_user")
        session_id = msg.get("session_id", "default_session")
        # Connect to managed session if agent_engine_id is set.
        app_id = agent_name
        # SSE endpoint
        session = session_service.get_session(
            app_name=app_id, user_id=user_id, session_id=session_id
        )

        # 新增代码
        if not session:
            logger.info("New session created: %s", session_id)
            session = session_service.create_session(
                app_name=app_id,
                user_id=user_id,
                state={},
                session_id=session_id,
            )
        if not session:
            logger.error(f"session not found: {session_id}")

        live_request_queue = LiveRequestQueue()

        async def forward_events():
            runner = _get_runner(agent_name)
            async for event in runner.run_live(
                session=session, live_request_queue=live_request_queue
            ):
                ws.send(
                    event.model_dump_json(exclude_none=True, by_alias=True), text=True
                )

        async def process_messages():
            try:
                while True:
                    data = ws.recv()
                    logger.info(f"收到来自客户端的消息2: {data}")
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
        # except WebSocketDisconnect:
        #     logger.info("Client disconnected during process_messages.")
        except Exception as e:
            logger.exception("Error during live websocket communication: %s", e)
            traceback.print_exc()
        finally:
            for task in pending:
                task.cancel()

        # try:
        #     stream_mode = StreamingMode.SSE  # StreamingMode.NONE
        #     runner = _get_runner(agent_name)
        #     async for event in runner.run_async(
        #         user_id=user_id,
        #         session_id=session_id,
        #         new_message=new_message,
        #         run_config=RunConfig(streaming_mode=stream_mode),
        #     ):
        #         # Format as SSE data
        #         sse_event = event.model_dump_json(exclude_none=True, by_alias=True)
        #         logger.info("Generated event in agent run streaming: %s", sse_event)
        #         yield f"data: {sse_event}\n\n"
        # except Exception as e:
        #     logger.exception("Error in event_generator: %s", e)
        #     # You might want to yield an error event here
        #     yield f'data: {{"error": "{str(e)}"}}\n\n'
