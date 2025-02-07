import json
import logging
from typing import cast

from agents.ctx import AgentContext
from autogen_agentchat.base import TaskResult
from autogen_agentchat.messages import TextMessage
from mtmaisdk.clients.rest.models.ag_event_create import AgEventCreate
from mtmaisdk.clients.rest.models.agent_node_run_input import AgentNodeRunInput
from mtmaisdk.context.context import Context
from pydantic import BaseModel

from mtmai.ag.team_builder import TeamBuilder
from mtmai.agents.ctx import get_mtmai_context, init_mtmai_context
from mtmai.worker import wfapp

logger = logging.getLogger(__name__)


async def run_stream(task: str):
    team_builder = TeamBuilder()
    agent = await team_builder.create_demo_agent_stream1()
    # team_runner = TeamRunner()

    # async for event in team_runner.run_stream(
    async for event in agent.run_stream(
        task=task,
        # team_config=agent.dump_component()
    ):
        if isinstance(event, TextMessage):
            yield event.model_dump()
        # elif isinstance(event, ToolCallRequestEvent):
        #     yield f"0:{json.dumps(obj=jsonable_encoder(event.content))}\n"
        # elif isinstance(event, TeamResult):
        #     yield f"0:{json.dumps(obj=event.model_dump_json())}\n"

        elif isinstance(event, BaseModel):
            # yield f"2:{event.model_dump_json()}\n"
            yield event.model_dump()
        elif isinstance(event, TaskResult):
            # 最终的结果
            # yield event
            pass
        else:
            # yield f"2:{json.dumps(f'unknown event: {str(event)},type:{type(event)}')}\n"
            yield event.model_dump()


@wfapp.workflow(
    name="ag",
    on_events=["autogen-demo:run"],
    input_validator=AgentNodeRunInput,
)
class FlowAg:
    @wfapp.step(
        timeout="30m",
        # retries=1
    )
    async def step_entry(self, hatctx: Context):
        init_mtmai_context(hatctx)
        ctx: AgentContext = get_mtmai_context()
        input = cast(AgentNodeRunInput, hatctx.workflow_input())
        tenant_id = ctx.getTenantId()
        if not tenant_id:
            raise ValueError("tenantId 不能为空")
        user_id = ctx.getUserId()
        if not user_id:
            raise ValueError("userId 不能为空")
        logger.info("当前租户: %s, 当前用户: %s", tenant_id, user_id)
        # 临时代码
        r = await hatctx.rest_client.aio.ag_events_api.ag_event_list(tenant=tenant_id)
        hatctx.log(r)

        # 获取模型配置
        user_messages = input.messages
        if len(user_messages) == 0:
            raise ValueError("No messages provided")
        task = user_messages[-1].content
        # task = "hello"
        logger.info("任务: %s", task)
        async for event in run_stream(task):
            hatctx.log(event)
            result = await hatctx.rest_client.aio.ag_events_api.ag_event_create(
                tenant=tenant_id,
                ag_event_create=AgEventCreate(
                    user_id=user_id,
                    data=event,
                    framework="autogen",
                    stepRunId=hatctx.step_run_id,
                    meta={},
                ),
            )

            hatctx.log(result)
            stream_bytes = json.dumps(event)
            hatctx.put_stream(stream_bytes)
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
