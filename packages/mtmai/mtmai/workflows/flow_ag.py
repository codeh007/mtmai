import logging
from typing import cast

from agents.ctx import AgentContext
from mtmaisdk.clients.rest.models.ag_event_create import AgEventCreate
from mtmaisdk.clients.rest.models.agent_run_input import AgentRunInput
from mtmaisdk.clients.rest.models.flow_ag_payload import FlowAgPayload
from mtmaisdk.context.context import Context
from pydantic import BaseModel

from mtmai.agents.ctx import get_mtmai_context, init_mtmai_context
from mtmai.worker import wfapp

logger = logging.getLogger(__name__)


@wfapp.workflow(
    name="ag",
    on_events=["ag:run"],
    input_validator=AgentRunInput,
)
class FlowAg:
    @wfapp.step(
        timeout="30m",
        # retries=1
    )
    async def step_entry(self, hatctx: Context):
        from mtmai.ag.team_runner import TeamRunner

        init_mtmai_context(hatctx)
        ctx: AgentContext = get_mtmai_context()
        input = cast(AgentRunInput, hatctx.workflow_input())
        tenant_id = ctx.getTenantId()
        if not tenant_id:
            raise ValueError("tenantId 不能为空")
        user_id = ctx.getUserId()
        if not user_id:
            raise ValueError("userId 不能为空")
        params = FlowAgPayload.model_validate(hatctx.input.get("params"))

        team_id = params.team_id
        if not team_id:
            raise ValueError("teamId 不能为空")

        if len(params.messages) == 0:
            raise ValueError("No messages provided")
        logger.info("当前租户: %s, 当前用户: %s", tenant_id, user_id)

        # 临时代码
        r = await hatctx.rest_client.aio.ag_events_api.ag_event_list(tenant=tenant_id)
        hatctx.log(r)

        # 获取聊天消息
        if len(params.messages) == 0:
            raise ValueError("No messages provided")
        task = params.messages[-1].content
        team_runner = TeamRunner()
        async for event in team_runner.run_stream_v2(ctx, task, team_id):
            hatctx.log(event)

            _event = event
            if isinstance(event, BaseModel):
                _event = event.model_dump()
            result = await hatctx.rest_client.aio.ag_events_api.ag_event_create(
                tenant=tenant_id,
                ag_event_create=AgEventCreate(
                    user_id=user_id,
                    data=_event,
                    framework="autogen",
                    stepRunId=hatctx.step_run_id,
                    meta={},
                ),
            )
            hatctx.log(result)
            hatctx.put_stream(event)
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
