from autogen_agentchat.base import Team
from autogen_agentchat.messages import TextMessage
from mtlibs.autogen_utils.cancel_token import MtCancelToken
from mtmai.clients.rest.models.flow_names import FlowNames
from mtmai.clients.rest.models.flow_team_input import FlowTeamInput
from mtmai.context.context import Context
from mtmai.hatchet import Hatchet
from mtmai.mtlibs.autogen_utils.component_loader import ComponentLoader

mtmapp = Hatchet()


@mtmapp.workflow(
    name=FlowNames.TEAM,
    on_events=[FlowNames.TEAM],
)
class FlowTeam:
    @mtmapp.step(timeout="60m")
    async def step0(self, hatctx: Context):
        input = FlowTeamInput.from_dict(hatctx.input)
        team = ComponentLoader.load_component(input.component, expected=Team)
        task = TextMessage(content=input.task, source="user")
        result = await team.run(task=task, cancellation_token=MtCancelToken())
        return result
