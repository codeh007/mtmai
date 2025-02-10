import logging
from typing import cast

from ag import team_builder
from agents.ctx import AgentContext
from mtmaisdk.clients.rest.models.agent_node_run_input import AgentNodeRunInput
from mtmaisdk.context.context import Context

from mtmai.agents.ctx import get_mtmai_context, init_mtmai_context
from mtmai.worker import wfapp

logger = logging.getLogger(__name__)


@wfapp.workflow(
    name="tenant",
    on_events=["tenant:run"],
    # input_validator=AgentNodeRunInput,
)
class FlowTenant:
    """
    租户工作流
    """

    @wfapp.step(
        timeout="30m",
        # retries=1
    )
    async def step_reset_tenant(self, hatctx: Context):
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

        # 获取模型配置
        logger.info("获取模型配置")
        r = await hatctx.rest_client.aio.model_api.model_list(tenant=tenant_id)
        hatctx.log(r)

        return {"result": "success"}

    @wfapp.step(timeout="1m", retries=1, parents=["step_reset_tenant"])
    async def add_teams(self, hatctx: Context):
        """添加默认团队"""
        builder = team_builder.TeamBuilder()

        travel_team = await builder.create_travel_agent()
        # team1 = demo_team.()
        team_component = travel_team.dump_component()

        return {"result": "success"}
