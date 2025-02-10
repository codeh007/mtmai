import logging
from typing import cast

from agents.ctx import AgentContext
from mtmaisdk.clients.rest.models.agent_run_input import AgentRunInput
from mtmaisdk.context.context import Context

from mtmai.agents.ctx import get_mtmai_context, init_mtmai_context
from mtmai.worker import wfapp

logger = logging.getLogger(__name__)


@wfapp.workflow(
    name="tenant",
    on_events=["tenant:run"],
    input_validator=AgentRunInput,
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
        r = await hatctx.rest_client.aio.model_api.model_list(tenant=tenant_id)
        hatctx.log(r)

        return {"result": "success"}
