import json
import logging
from typing import cast

from agents.ctx import AgentContext
from mtmaisdk.clients.rest.models.ag_event_create import AgEventCreate
from mtmaisdk.clients.rest.models.agent_node_run_input import AgentNodeRunInput
from mtmaisdk.context.context import Context

from mtmai.agents.ctx import get_mtmai_context, init_mtmai_context
from mtmai.worker import wfapp

logger = logging.getLogger(__name__)


@wfapp.workflow(
    name="ag",
    on_events=["ag:run"],
    input_validator=AgentNodeRunInput,
)
class FlowAg:
    @wfapp.step(
        timeout="30m",
        # retries=1
    )
    async def step_entry(self, hatctx: Context):
        from ..ag.team_runner import TeamRunner

        init_mtmai_context(hatctx)
        ctx: AgentContext = get_mtmai_context()
        input = cast(AgentNodeRunInput, hatctx.workflow_input())
        tenant_id = ctx.getTenantId()
        if not tenant_id:
            raise ValueError("tenantId 不能为空")
        user_id = ctx.getUserId()
        if not user_id:
            raise ValueError("userId 不能为空")
        team_id = input.team_id
        if not team_id:
            raise ValueError("teamId 不能为空")
        logger.info("当前租户: %s, 当前用户: %s", tenant_id, user_id)

        # 临时代码
        r = await hatctx.rest_client.aio.ag_events_api.ag_event_list(tenant=tenant_id)
        hatctx.log(r)

        # 获取模型配置
        user_messages = input.messages
        if len(user_messages) == 0:
            raise ValueError("No messages provided")
        task = user_messages[-1].content

        team_runner = TeamRunner()
        async for event in team_runner.run_stream_v2(ctx, task, team_id):
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

    # @wfapp.step(timeout="1m", retries=1, parents=["step_b"])
    # async def step_b_2(self, hatctx: Context):
    #     hatctx.log("stepB2")
    #     # raise Exception("stepB2 error")
    #     return {"result": "success"}

    # @wfapp.step(timeout="1m", retries=1, parents=["step_b_2"])
    # async def step_b_3(self, hatctx: Context):
    #     hatctx.log("stepB3")
    #     # raise Exception("stepB3 error")
    #     return {"result": "success"}

    # @wfapp.step(timeout="1m", retries=1, parents=["step_entry"])
    # async def step_c(self, hatctx: Context):
    #     hatctx.log("stepC")
    #     return {"result": "success"}
    #     return {"result": "success"}
