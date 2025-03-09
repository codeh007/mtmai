from mtmai.agents.cancel_token import MtCancelToken
from mtmai.clients.rest.models.instagram_task import InstagramTask
from mtmai.context.context import Context
from mtmai.teams.instagram_team import InstagramTeam
from mtmai.worker_app import mtmapp


@mtmapp.workflow(
    name="instagram",
    on_events=["instagram:run"],
)
class FlowInstagram:
    @mtmapp.step(timeout="60m")
    async def step_entry(self, hatctx: Context):
        instagram_agent = InstagramTeam()

        result = await instagram_agent.run(
            task=InstagramTask.model_validate(hatctx.input),
            cancellation_token=MtCancelToken(),
        )
        return result
