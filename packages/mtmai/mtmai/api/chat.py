import json

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


@router.api_route(path="/test_m1", methods=["GET", "POST"])
async def test_m1(r: Request):
    # 测试 megentic one agent
    try:
        model_client = get_oai_Model()
        assistant = AssistantAgent(
            "Assistant",
            model_client=model_client,
        )
        team = MagenticOneGroupChat([assistant], model_client=model_client)
        await Console(
            team.run_stream(task="Provide a different proof for Fermat's Last Theorem")
        )

    except Exception as e:
        LOG.error("Chat error", error=str(e))
        return {"error": str(e)}
