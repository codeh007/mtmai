from autogen_agentchat.base import Team
from autogen_agentchat.messages import TextMessage
from mtmai.agents.cancel_token import MtCancelToken
from mtmai.clients.rest.models.flow_names import FlowNames
from mtmai.clients.rest.models.flow_team_input import FlowTeamInput
from mtmai.context.context import Context
from mtmai.hatchet import Hatchet

mtmapp = Hatchet()


@mtmapp.workflow(
    name=FlowNames.TEAM,
    on_events=[FlowNames.TEAM],
)
class FlowTeam:
    @mtmapp.step(timeout="60m")
    async def step0(self, hatctx: Context):
        input = FlowTeamInput.from_dict(hatctx.input)
        cancellation_token = MtCancelToken()

        component_dict = input.component.to_dict()
        team = Team.load_component(component_dict)
        task = TextMessage(content=input.task, source="user")
        return await team.run(task=task, cancellation_token=cancellation_token)
