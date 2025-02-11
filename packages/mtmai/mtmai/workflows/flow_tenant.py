import logging
from typing import cast

from ag.team_builder.travel_builder import TeamBuilder
from agents.ctx import AgentContext
from mtmaisdk.clients.rest.models.agent_run_input import AgentRunInput
from mtmaisdk.clients.rest.models.team import Team
from mtmaisdk.clients.rest.models.team_component import TeamComponent
from mtmaisdk.context.context import Context

from mtmai.agents.ctx import get_mtmai_context, init_mtmai_context
from mtmai.worker import wfapp

logger = logging.getLogger(__name__)


@wfapp.workflow(
    name="tenant",
    on_events=["tenant:run"],
    # input_validator=AgentRunInput,
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
        tenant_id = ctx.getTenantId()
        if not tenant_id:
            raise ValueError("tenantId 不能为空")
        user_id = ctx.getUserId()
        if not user_id:
            raise ValueError("userId 不能为空")
        logger.info("当前租户: %s, 当前用户: %s", tenant_id, user_id)

        input = cast(AgentRunInput, hatctx.workflow_input())

        # 获取模型配置
        logger.info("获取模型配置")
        r = await hatctx.rest_client.aio.model_api.model_get(
            tenant=tenant_id, model="default"
        )
        hatctx.log(r)

        model_config = r.config
        team_builder = TeamBuilder()
        team1 = await team_builder.create_travel_agent(model_config)
        hatctx.log(team1)

        # 保存 team
        team_comp = team1.dump_component().model_dump()
        r = await hatctx.rest_client.aio.team_api.team_upsert(
            tenant=tenant_id,
            team_id=team1._team_id,
            team2=Team(
                label="travel_agent",
                description=team1.component_description or "",
                component=TeamComponent(**team_comp),
            ),
        )
        hatctx.log(r)
        return {"result": "success"}
