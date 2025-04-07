from clients.rest.models.flow_names import FlowNames
from mtmai.agents.cancel_token import MtCancelToken
from mtmai.clients.rest.models.mt_ag_event import MtAgEvent
from mtmai.clients.rest.models.user_team_config import UserTeamConfig
from mtmai.context.context import Context
from mtmai.teams.team_user import UserTeam
from mtmai.worker_app import mtmapp


@mtmapp.workflow(
    name=FlowNames.USER,
    on_events=[FlowNames.USER],
)
class FlowUser:
    @mtmapp.step(timeout="60m")
    async def step0(self, hatctx: Context):
        input = MtAgEvent.from_dict(hatctx.input)
        cancellation_token = MtCancelToken()
        team = UserTeam._from_config(UserTeamConfig())
        return await team.run(task=input, cancellation_token=cancellation_token)
