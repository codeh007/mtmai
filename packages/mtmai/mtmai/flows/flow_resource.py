from autogen_agentchat.base import TaskResult
from loguru import logger
from mtmai.agents.cancel_token import MtCancelToken
from mtmai.agents.team_builder.resource_team_builder import ResourceTeamBuilder
from mtmai.clients.rest.models.agent_run_input import AgentRunInput
from mtmai.context.context import Context
from mtmai.context.context_client import TenantClient
from mtmai.worker_app import mtmapp


@mtmapp.workflow(
    name="resource",
    on_events=["resource:run"],
)
class FlowResource:
    @mtmapp.step(timeout="60m")
    async def step_entry(self, hatctx: Context):
        input = AgentRunInput.model_validate(hatctx.input)
        builder = ResourceTeamBuilder()
        team = await builder.create_team(input)

        tenant_client = TenantClient()
        cancellation_token = MtCancelToken()
        async for event in team.run_stream(
            task=input,
            cancellation_token=cancellation_token,
        ):
            if cancellation_token and cancellation_token.is_cancelled():
                break
            if isinstance(event, TaskResult):
                result = event
                return result
            await tenant_client.emit(event)

        logger.info("(FlowResource)工作流结束")
