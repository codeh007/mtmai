from autogen_agentchat.base import TaskResult
from mtmai.agents.cancel_token import MtCancelToken
from mtmai.agents.team_builder.resource_team_builder import ResourceTeamBuilder
from mtmai.clients.rest.models.instagram_task import InstagramTask
from mtmai.context.context import Context
from mtmai.worker_app import mtmapp

from ..context.context_client import TenantClient


@mtmapp.workflow(
    name="instagram",
    on_events=["instagram:run"],
)
class FlowInstagram:
    @mtmapp.step(timeout="60m")
    async def step_entry(self, hatctx: Context):
        input = InstagramTask.model_validate(hatctx.input)
        builder = ResourceTeamBuilder()
        team = await builder.create_team(input.resource_id)

        tenant_client = TenantClient()
        # result = await team.run(
        #     task=input.content,
        #     cancellation_token=MtCancelToken(),
        # )
        async for event in team.run_stream(
            task=input.content,
            cancellation_token=MtCancelToken(),
        ):
            # if cancellation_token and cancellation_token.is_cancelled():
            #         break
            if isinstance(event, TaskResult):
                result = event
                return result
            await tenant_client.emit(event)
