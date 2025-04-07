from mtmai.agents.cancel_token import MtCancelToken
from mtmai.clients.rest.models.mt_ag_event import MtAgEvent
from mtmai.context.context import Context
from mtmai.teams.team_tooluse import TooluseTeam, TooluseTeamConfig
from mtmai.worker_app import mtmapp


@mtmapp.workflow(
    name="tooluse",
    on_events=["tooluse"],
)
class FlowTooluse:
    @mtmapp.step(timeout="60m")
    async def step0(self, hatctx: Context):
        input = MtAgEvent.from_dict(hatctx.input)
        cancellation_token = MtCancelToken()
        team = TooluseTeam._from_config(TooluseTeamConfig())
        return await team.run(task=input, cancellation_token=cancellation_token)
