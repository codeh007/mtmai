import json

from autogen_agentchat.messages import TextMessage
from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from loguru import logger
from pydantic import BaseModel

from ..agents.ag.team_builder import TeamBuilder
from ..agents.ag.team_runner import TeamRunner
from ..gomtmclients.rest.models.chat_req import ChatReq

router = APIRouter()


async def run_stream(task: str):
    try:
        team_builder = TeamBuilder()
        team = await team_builder.create_demo_team()
        team_runner = TeamRunner()

        async for event in team_runner.run_stream(
            task=task, team_config=team.dump_component()
        ):
            if isinstance(event, TextMessage):
                yield f"2:{event.model_dump_json()}\n"
            # elif isinstance(event, ToolCallRequestEvent):
            #     yield f"0:{json.dumps(obj=jsonable_encoder(event.content))}\n"
            # elif isinstance(event, TeamResult):
            #     yield f"0:{json.dumps(obj=event.model_dump_json())}\n"

            elif isinstance(event, BaseModel):
                yield f"2:{event.model_dump_json()}\n"
            else:
                yield f"2:{json.dumps(f'unknown event: {str(event)},type:{type(event)}')}\n"
    except Exception as e:
        logger.exception("Streaming error")
        yield f"2:{json.dumps({'error': str(e)})}\n"


@router.api_route(path="/tenants/{tenant}/chat", methods=["GET", "POST"])
async def chat(r: ChatReq):
    try:
        user_messages = r.messages
        if len(user_messages) == 0:
            raise HTTPException(status_code=400, detail="No messages provided")
        task = user_messages[-1].content

        return StreamingResponse(
            content=run_stream(task), media_type="text/event-stream"
        )

    except Exception as e:
        logger.exception("Chat error")
        raise HTTPException(status_code=500, detail=str(e))


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
#         return {"error": str(e)}
#         return {"error": str(e)}
#         return {"error": str(e)}
#         return {"error": str(e)}
