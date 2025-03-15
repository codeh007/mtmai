from autogen_agentchat.base import TaskResult
from loguru import logger
from mtmai.agents.cancel_token import MtCancelToken
from mtmai.clients.rest.models.agent_run_input import AgentRunInput
from mtmai.clients.rest.models.component_types import ComponentTypes
from mtmai.clients.rest.models.mt_task_result import MtTaskResult
from mtmai.context.context import Context
from mtmai.context.context_client import TenantClient
from mtmai.context.ctx import get_chat_session_id_ctx, get_tenant_id
from mtmai.teams.instagram_team import InstagramTeam
from mtmai.worker_app import mtmapp


@mtmapp.workflow(
    name="ag",
    on_events=["ag:run"],
)
class FlowAg:
    @mtmapp.step(timeout="60m")
    async def step_entry(self, hatctx: Context):
        # return await hatctx.sys_team.run_stream(
        #     task=AgentRunInput.model_validate(hatctx.input),
        #     cancellation_token=MtCancelToken(),
        # )

        input = AgentRunInput.model_validate(hatctx.input)
        cancellation_token = MtCancelToken()
        # await hatctx.sys_team.run_team(input, cancellation_token)

        tenant_client = TenantClient()
        session_id = get_chat_session_id_ctx()

        # result = await self._runtime.send_message(
        #     message=input,
        #     recipient=AgentId(type=team_runner_topic_type, key=session_id),
        #     cancellation_token=cancellation_token,
        # )

        tid = get_tenant_id()
        if not tid:
            raise ValueError("tenant_id is required")
        component_data = await tenant_client.ag.coms_api.coms_get(
            tenant=tid,
            com=input.component_id,
        )
        logger.info(f"component data: {component_data}")

        if component_data.component_type == ComponentTypes.TEAM:
            # team = Team.load_component(component_data)
            team = InstagramTeam.load_component(component_data)
            # return team
        else:
            raise ValueError(f"不支持组件类型: {component_data.component_type}")
        async for event in team.run_stream(
            task=input.content,
            cancellation_token=cancellation_token,
        ):
            if isinstance(event, TaskResult):
                result = event
                mt_result = MtTaskResult(
                    messages=result.messages,
                    stop_reason=result.stop_reason,
                )
                tenant_client.emit(mt_result)
                break
            await tenant_client.emit(event)
        # logger.info("团队运行完全结束")

        logger.info(f"(FlowResource)工作流结束,{hatctx.step_run_id}")
