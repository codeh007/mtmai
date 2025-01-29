import json
from typing import Any

import structlog
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.messages import TextMessage
from autogen_agentchat.teams import MagenticOneGroupChat
from autogen_agentchat.ui import Console
from fastapi import APIRouter, Request
from fastapi.responses import StreamingResponse

from ..agents.ag.model_client import get_oai_Model

router = APIRouter()
LOG = structlog.get_logger()


@router.api_route(path="", methods=["GET", "POST"])
async def chat(r: Request):
    try:
        data = await r.json()
        user_messages = data.get("messages", [])
        user_message = user_messages[-1].get("content", "")
        assistant = AssistantAgent(name="assistant", model_client=get_oai_Model())

        async def chat_stream():
            chat_response = assistant.run_stream(task=user_message)
            async for chunk in chat_response:
                if isinstance(chunk, TextMessage):
                    yield f"0:{json.dumps(chunk.content)}\n"

        return StreamingResponse(chat_stream(), media_type="text/event-stream")

    except Exception as e:
        LOG.error("Chat error", error=str(e))
        return {"error": str(e)}


class LoggingModelClient:
    def __init__(self, wrapped_client):
        self.wrapped_client = wrapped_client

    async def create(self, *args: Any, **kwargs: Any) -> Any:
        LOG.info("OpenAI API Request", request_args=args, request_kwargs=kwargs)
        try:
            response = await self.wrapped_client.create(*args, **kwargs)

            # 修正json格式, 原因:对于 llama3 输出的json字符串,可能不严格
            if kwargs.get("json_output", True):
                if isinstance(response.content, str):
                    if response.content.startswith("```json"):
                        response.content = response.content[7:-3]
                    if response.content.startswith("```"):
                        response.content = response.content[6:-3]
                    if response.content.endswith("```"):
                        response.content = response.content[:-3]
                    response.content = json.dumps(response.content)

            LOG.info("OpenAI API Response", content=response.content)
            return response
        except Exception as e:
            LOG.error("OpenAI API Error", error=str(e), error_type=type(e).__name__)
            raise


@router.api_route(path="/test_m1", methods=["GET", "POST"])
async def test_m1(r: Request):
    # 测试 megentic one agent
    try:
        model_client = get_oai_Model()
        logging_client = LoggingModelClient(model_client)

        assistant = AssistantAgent(
            "Assistant",
            model_client=logging_client,
        )
        team = MagenticOneGroupChat([assistant], model_client=logging_client)
        await Console(
            team.run_stream(task="Provide a different proof for Fermat's Last Theorem")
        )

    except Exception as e:
        LOG.error("Chat error", error=str(e))
        return {"error": str(e)}
