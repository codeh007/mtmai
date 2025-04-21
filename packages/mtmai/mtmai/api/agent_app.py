# import asyncio
# import importlib
# import json
# import os
# import re
# import sys
# import traceback
# import typing
# from pathlib import Path
# from typing import Any, List, Literal, Optional

# import click
# import graphviz
# from fastapi import FastAPI, HTTPException, Query
# from fastapi.middleware.cors import CORSMiddleware
# from fastapi.responses import FileResponse, RedirectResponse, StreamingResponse
# from fastapi.staticfiles import StaticFiles
# from fastapi.websockets import WebSocket, WebSocketDisconnect
# from google.adk.agents import RunConfig
# from google.adk.agents.live_request_queue import LiveRequest, LiveRequestQueue
# from google.adk.agents.llm_agent import Agent
# from google.adk.agents.run_config import StreamingMode
# from google.adk.artifacts import InMemoryArtifactService
# from google.adk.cli.cli_eval import (
#     EVAL_SESSION_ID_PREFIX,
#     EvalMetric,
#     EvalMetricResult,
#     EvalStatus,
# )
# from google.adk.cli.utils import create_empty_state, envs, evals
# from google.adk.events.event import Event
# from google.adk.runners import Runner
# from google.adk.sessions import DatabaseSessionService
# from google.adk.sessions.in_memory_session_service import InMemorySessionService
# from google.adk.sessions.session import Session
# from google.adk.sessions.vertex_ai_session_service import VertexAiSessionService
# from google.genai import types
# from loguru import logger
# from opentelemetry import trace
# from opentelemetry.exporter.cloud_trace import CloudTraceSpanExporter
# from opentelemetry.sdk.trace import ReadableSpan, TracerProvider, export
# from pydantic import BaseModel, ValidationError
# from starlette.types import Lifespan

# from mtmai.core.config import settings
# @app.get("/list-apps")
# def list_apps() -> list[str]:
#     base_path = Path.cwd() / agent_dir
#     if not base_path.exists():
#         raise HTTPException(status_code=404, detail="Path not found")
#     if not base_path.is_dir():
#         raise HTTPException(status_code=400, detail="Not a directory")
#     agent_names = [
#         x
#         for x in os.listdir(base_path)
#         if os.path.isdir(os.path.join(base_path, x))
#         and not x.startswith(".")
#         and x != "__pycache__"
#     ]
#     agent_names.sort()
#     return agent_names
