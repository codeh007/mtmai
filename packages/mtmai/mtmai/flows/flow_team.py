from autogen_agentchat.base import Team
from autogen_agentchat.messages import TextMessage
from mtmai.agents.cancel_token import MtCancelToken
from mtmai.clients.rest.models.ag_state_upsert import AgStateUpsert
from mtmai.clients.rest.models.flow_names import FlowNames
from mtmai.clients.rest.models.flow_team_input import FlowTeamInput
from mtmai.clients.rest.models.state_type import StateType
from mtmai.clients.tenant_client import TenantClient
from mtmai.context.context import Context
from mtmai.context.ctx import get_chat_session_id_ctx
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
        tenant_client = TenantClient()
        session_id = get_chat_session_id_ctx()
        input = FlowTeamInput.from_dict(hatctx.input)
        team = ComponentLoader.load_component(input.component, expected=Team)
        task = TextMessage(content=input.task, source="user")
        result = await team.run(task=task, cancellation_token=MtCancelToken())

        if team and hasattr(team, "_participants"):
            for agent in team._participants:
                if hasattr(agent, "close"):
                    await agent.close()

        team_state = await team.save_state()
        await tenant_client.ag_state_api.ag_state_upsert(
            tenant=tenant_client.tenant_id,
            ag_state_upsert=AgStateUpsert(
                type=StateType.TEAMSTATE.value,
                chatId=session_id,
                state=team_state,
                topic="default",
                source="default",
            ),
        )
        return result
