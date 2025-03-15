from autogen_agentchat.base import TaskResult
from fastapi.encoders import jsonable_encoder
from loguru import logger
from mtmai.agents.cancel_token import MtCancelToken
from mtmai.clients.rest.models.agent_run_input import AgentRunInput
from mtmai.clients.rest.models.component_types import ComponentTypes
from mtmai.context.context import Context
from mtmai.context.context_client import TenantClient
from mtmai.context.ctx import get_tenant_id
from mtmai.teams.instagram_team import InstagramTeam
from mtmai.worker_app import mtmapp


@mtmapp.workflow(
    name="ag",
    on_events=["ag:run"],
)
class FlowAg:
    @mtmapp.step(timeout="60m")
    async def step_entry(self, hatctx: Context):
        input = AgentRunInput.model_validate(hatctx.input)
        cancellation_token = MtCancelToken()
        tenant_client = TenantClient()
        tid = get_tenant_id()
        if not tid:
            raise ValueError("tenant_id is required")
        component_data = await tenant_client.ag.coms_api.coms_get(
            tenant=tid,
            com=input.component_id,
        )
        logger.info(f"component data: {component_data}")

        if component_data.component_type == ComponentTypes.TEAM:
            team = InstagramTeam.load_component(component_data)
        else:
            raise ValueError(f"不支持组件类型: {component_data.component_type}")
        async for event in team.run_stream(
            task=input.content,
            cancellation_token=cancellation_token,
        ):
            if isinstance(event, TaskResult):
                return jsonable_encoder(event)
                # mt_result = MtTaskResult(
                #     messages=result.messages,
                #     stop_reason=result.stop_reason,
                # )
                # tenant_client.emit(mt_result)
                # break
            # await tenant_client.emit(event)

        # logger.info(f"(FlowResource)工作流结束,{hatctx.step_run_id}")
