import json
from typing import cast

from autogen_agentchat.messages import TextMessage
from fastapi import HTTPException
from loguru import logger
from mtmaisdk.clients.rest.models import PostizState
from mtmaisdk.context.context import Context
from pydantic import BaseModel

from mtmai.agents.ctx import init_mtmai_context
from mtmai.worker import wfapp

from ..ag.team_builder import TeamBuilder


async def run_stream(task: str):
    try:
        team_builder = TeamBuilder()
        # team = await team_builder.create_demo_team()

        agent = await team_builder.create_demo_agent_stream1()
        # team_runner = TeamRunner()

        # async for event in team_runner.run_stream(
        async for event in agent.run_stream(
            task=task,
            # team_config=agent.dump_component()
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


@wfapp.workflow(
    name="ag",
    on_events=["autogen-demo:run"],
    # input_validator=PostizState,
)
class FlowAutogenDemo:
    @wfapp.step(timeout="30m", retries=1)
    async def step_entry(self, hatctx: Context):
        init_mtmai_context(hatctx)

        input: PostizState = cast(PostizState, hatctx.workflow_input())
        hatctx.log(input)
        # outoput = await assisant_graph.AssistantGraph.run(input)

        try:
            # user_messages = r.messages
            # if len(user_messages) == 0:
            #     raise HTTPException(status_code=400, detail="No messages provided")
            # task = user_messages[-1].content
            task = "hello"
            async for event in run_stream(task):
                hatctx.log(event)

        except Exception as e:
            logger.exception("Chat error")
            hatctx.log(str(e))
            raise HTTPException(status_code=500, detail=str(e))

        return {"result": "success"}
