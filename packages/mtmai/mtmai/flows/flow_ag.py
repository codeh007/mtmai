from autogen_agentchat.base import TaskResult
from loguru import logger
from mtmai.agents.cancel_token import MtCancelToken
from mtmai.clients.rest.models.agent_run_input import AgentRunInput
from mtmai.clients.rest.models.component_types import ComponentTypes
from mtmai.clients.rest.models.flow_names import FlowNames
from mtmai.context.context import Context
from mtmai.context.context_client import TenantClient
from mtmai.context.ctx import get_chat_session_id_ctx, get_tenant_id
from mtmai.teams.instagram_team import InstagramTeam
from mtmai.worker_app import mtmapp


@mtmapp.workflow(
    name=FlowNames.AG,
    on_events=[f"{FlowNames.AG}"],
)
class FlowAg:
    @mtmapp.step(timeout="60m")
    async def step_entry(self, hatctx: Context):
        input = AgentRunInput.model_validate(hatctx.input)
        cancellation_token = MtCancelToken()
        tenant_client = TenantClient()
        session_id = get_chat_session_id_ctx()
        tid = get_tenant_id()
        if not tid:
            raise ValueError("tenant_id is required")
        try:
            component_data = await tenant_client.ag.coms_api.coms_get(
                tenant=tid,
                com=input.component_id,
            )
            logger.info(f"component data: {component_data}")
        except Exception as e:
            logger.exception(f"获取组件数据失败: {e}")
            raise e
        if component_data.component_type == ComponentTypes.TEAM:
            team = InstagramTeam.load_component(component_data)
        else:
            raise ValueError(f"不支持组件类型: {component_data.component_type}")

        task_result = None
        async for event in team.run_stream(
            task=input.content,
            cancellation_token=cancellation_token,
        ):
            if isinstance(event, TaskResult):
                logger.info(f"工作流完成: {event}")
                task_result = event
                break
                # mt_result = MtTaskResult(
                #     messages=result.messages,
                #     stop_reason=result.stop_reason,
                # )
                # tenant_client.emit(mt_result)
                # break
            # await tenant_client.emit(event)
        if team and hasattr(team, "_participants"):
            for agent in team._participants:
                if hasattr(agent, "close"):
                    await agent.close()

        await tenant_client.ag.save_team_state(
            componentId=input.component_id,
            tenant_id=tid,
            chat_id=session_id,
            state=await team.save_state(),
        )

        logger.info(f"(FlowAg)工作流结束,{hatctx.step_run_id}\n{task_result}")
        return task_result
