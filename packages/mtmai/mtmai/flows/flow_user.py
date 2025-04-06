from loguru import logger
from mtmai.agents.cancel_token import MtCancelToken
from mtmai.clients.rest.models.agent_run_input import AgentRunInput
from mtmai.clients.rest.models.flow_instagram_input import FlowInstagramInput
from mtmai.clients.rest.models.flow_names import FlowNames
from mtmai.clients.rest.models.social_add_followers_input import SocialAddFollowersInput
from mtmai.clients.rest.models.social_login_input import SocialLoginInput
from mtmai.clients.tenant_client import TenantClient
from mtmai.context.context import Context
from mtmai.context.ctx import get_chat_session_id_ctx, get_tenant_id
from mtmai.worker_app import mtmapp


@mtmapp.workflow(
    name=FlowNames.USER,
    on_events=[f"{FlowNames.USER}"],
)
class FlowUser:
    @mtmapp.step(timeout="60m")
    async def step0(self, hatctx: Context):
        input = AgentRunInput.from_dict(hatctx.input)
        cancellation_token = MtCancelToken()
        tenant_client = TenantClient()
        session_id = get_chat_session_id_ctx()
        tid = get_tenant_id()
        if not tid:
            raise ValueError("tenant_id is required")

        if isinstance(input.input.actual_instance, FlowInstagramInput):
            return await hatctx.aio.spawn_workflow(
                FlowNames.INSTAGRAM, input.input.actual_instance.model_dump()
            )
        elif isinstance(input.input.actual_instance, SocialLoginInput):
            workflowRunRef = await hatctx.aio.spawn_workflow(
                FlowNames.INSTAGRAM, input.input.actual_instance.model_dump()
            )
            logger.info(f"workflowRunRef: {workflowRunRef}")
        elif isinstance(input.input.actual_instance, SocialAddFollowersInput):
            result = await hatctx.aio.spawn_workflow(
                FlowNames.INSTAGRAM, input.input.actual_instance.model_dump()
            )
            logger.info(f"result: {result}")
        else:
            raise ValueError("Invalid input type")

        return {"state": "user"}
