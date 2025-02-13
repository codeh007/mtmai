# import json

# from autogen_agentchat.messages import TextMessage
from fastapi import APIRouter
# from loguru import logger
# from pydantic import BaseModel

# from mtmai.agents.team_builder.travel_builder import TravelTeamBuilder
# from mtmai.agents.team_runner import TeamRunner

router = APIRouter()


# async def run_stream(task: str):
#     try:
#         team_builder = TravelTeamBuilder()
#         team = await team_builder.create_demo_team()
#         team_runner = TeamRunner()

#         async for event in team_runner.run_stream(
#             task=task, team_config=team.dump_component()
#         ):
#             if isinstance(event, TextMessage):
#                 yield f"2:{event.model_dump_json()}\n"
#             # elif isinstance(event, ToolCallRequestEvent):
#             #     yield f"0:{json.dumps(obj=jsonable_encoder(event.content))}\n"
#             # elif isinstance(event, TeamResult):
#             #     yield f"0:{json.dumps(obj=event.model_dump_json())}\n"

#             elif isinstance(event, BaseModel):
#                 yield f"2:{event.model_dump_json()}\n"
#             else:
#                 yield f"2:{json.dumps(f'unknown event: {str(event)},type:{type(event)}')}\n"
#     except Exception as e:
#         logger.exception("Streaming error")
#         yield f"2:{json.dumps({'error': str(e)})}\n"
