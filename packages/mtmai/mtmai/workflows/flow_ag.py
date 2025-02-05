import json
import logging
from typing import cast

from agents.ctx import AgentContext
from autogen_agentchat.messages import TextMessage
from fastapi import HTTPException
from mtmaisdk.clients.rest.models import PostizState
from mtmaisdk.context.context import Context
from pydantic import BaseModel

from mtmai.ag.team_builder import TeamBuilder
from mtmai.agents.ctx import get_mtmai_context, init_mtmai_context
from mtmai.worker import wfapp

# from loguru import logger


logger = logging.getLogger(__name__)


async def run_stream(task: str):
    # try:
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
    # except Exception as e:
    #     logger.exception("Streaming error")
    #     yield f"2:{json.dumps({'error': str(e)})}\n"


@wfapp.workflow(
    name="ag",
    on_events=["autogen-demo:run"],
    # input_validator=PostizState,
)
class FlowAg:
    @wfapp.step(timeout="30m", retries=1)
    async def step_entry(self, hatctx: Context):
        init_mtmai_context(hatctx)

        ctx: AgentContext = get_mtmai_context()
        ctx.log("FlowAg 启动")

        input: PostizState = cast(PostizState, hatctx.workflow_input())
        # hatctx.log(input)
        # ctx.log("输入: %s", input)
        # outoput = await assisant_graph.AssistantGraph.run(input)

        # 获取模型配置

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

    @wfapp.step(timeout="1m", retries=1, parents=["step_entry"])
    async def step_b(self, hatctx: Context):
        hatctx.log("stepB")
        hatctx.done()
        return {"result": "success"}

    @wfapp.step(timeout="1m", retries=1, parents=["step_b"])
    async def step_b_2(self, hatctx: Context):
        hatctx.log("stepB2")
        raise Exception("stepB2 error")

    @wfapp.step(timeout="1m", retries=1, parents=["step_b_2"])
    async def step_b_3(self, hatctx: Context):
        hatctx.log("stepB3")
        raise Exception("stepB3 error")

    @wfapp.step(timeout="1m", retries=1, parents=["step_entry"])
    async def step_c(self, hatctx: Context):
        hatctx.log("stepC")
        return {"result": "success"}
