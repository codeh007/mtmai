import json
from typing import Any

from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.messages import TextMessage
from fastapi import APIRouter, Request
from fastapi.responses import StreamingResponse
from json_repair import repair_json
from loguru import logger

from ..agents.ag.model_client import get_oai_Model

router = APIRouter()


@router.api_route(path="/tenants/{tenant}/chat", methods=["GET", "POST"])
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
        logger.error("Chat error", error=str(e))
        return {"error": str(e)}


class LoggingModelClient:
    def __init__(self, wrapped_client):
        self.wrapped_client = wrapped_client

    async def create(self, *args: Any, **kwargs: Any) -> Any:
        try:
            response = await self.wrapped_client.create(*args, **kwargs)
            if kwargs.get("json_output", False):
                # 修正json格式
                if isinstance(response.content, str):
                    response.content = repair_json(response.content)

            logger.info(
                "OpenAI API Response",
                request_args=args,
                request_kwargs=kwargs,
                response_content=response.content,
            )
            return response
        except Exception as e:
            logger.error("OpenAI API Error", error=str(e), error_type=type(e).__name__)
            raise


# @router.api_route(path="/test_m1", methods=["GET", "POST"])
# async def test_m1(r: Request):
#     from autogen_ext.agents.web_surfer import PlaywrightController

#     # 测试 megentic one agent
#     try:
#         model_client = get_oai_Model()
#         logging_client = LoggingModelClient(model_client)

#         assistant = AssistantAgent(
#             "Assistant",
#             model_client=logging_client,
#         )

#         surfer = PlaywrightController(
#             downloads_folder=".vol/WebSurfer",
#             model_client=model_client,
#         )

#         team = MagenticOneGroupChat([surfer], model_client=logging_client)
#         await Console(team.run_stream(task="用中文写一段关于马克龙的新闻"))

#     except Exception as e:
#         logger.error("Chat error", error=str(e))
#         return {"error": str(e)}
#         return {"error": str(e)}
