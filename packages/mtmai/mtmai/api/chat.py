import json

from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from loguru import logger

from ..agents.ag.team_builder import TeamBuilder
from ..agents.ag.team_runner import TeamRunner
from ..gomtmclients.rest.models.chat_req import ChatReq

router = APIRouter()


@router.api_route(path="/tenants/{tenant}/chat", methods=["GET", "POST"])
async def chat(r: ChatReq):
    try:
        user_messages = r.messages
        if len(user_messages) == 0:
            raise HTTPException(status_code=400, detail="No messages provided")
        task = user_messages[-1].content
        # 练习1: 简单调用

        # assistant = AssistantAgent(name="assistant", model_client=get_oai_Model())

        # async def chat_stream():
        #     chat_response = assistant.run_stream(task=user_message)
        #     async for chunk in chat_response:
        #         if isinstance(chunk, TextMessage):
        #             yield f"0:{json.dumps(chunk.content)}\n"

        # return StreamingResponse(chat_stream(), media_type="text/event-stream")

        team_builder = TeamBuilder()
        team = await team_builder.create_demo_team()
        team_runner = TeamRunner()

        async def stream_response():
            async for message in team_runner.run_stream(
                task=task, team_config=team.dump_component()
            ):
                yield f"0:{json.dumps(message)}\n"

        # stream
        return StreamingResponse(
            content=stream_response(), media_type="text/event-stream"
        )

    except Exception as e:
        logger.exception("Chat error")
        return {"error": str(e)}


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
