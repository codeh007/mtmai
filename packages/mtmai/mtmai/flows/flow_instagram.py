from mtmai.agents.cancel_token import MtCancelToken
from mtmai.agents.team_builder.resource_team_builder import ResourceTeamBuilder
from mtmai.clients.rest.models.instagram_task import InstagramTask
from mtmai.context.context import Context
from mtmai.worker_app import mtmapp


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
        result = await team.run(
            task=input.content,
            cancellation_token=MtCancelToken(),
        )
        return result
