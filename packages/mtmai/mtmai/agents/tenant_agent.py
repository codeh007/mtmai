import logging
from autogen_core import MessageContext, RoutedAgent, message_handler
from mtmaisdk.clients.rest.models.tenant_seed_req import TenantSeedReq
from mtmaisdk.clients.rest.models.team import Team
from mtmaisdk.clients.rest.models.team_component import TeamComponent
from mtmai.agents.team_builder.company_research import CompanyResearchTeamBuilder
from mtmai.agents.team_builder.travel_builder import TravelTeamBuilder
from autogen_core import RoutedAgent, message_handler, type_subscription
from mtmaisdk.clients.rest_client import AsyncRestApi

logger = logging.getLogger(__name__)

# @default_subscription
@type_subscription(topic_type="tenant")
class TenantAgent(RoutedAgent):
    def __init__(self) -> None:
        super().__init__("TenantAgent")
        # self.gomtmapi=gomtmapi

    @message_handler
    async def handle_tenant_message_type(self, message: TenantSeedReq, mctx: MessageContext) -> None:
        if not message.tenant_id or len(message.tenant_id) == 0:
            raise ValueError("tenantId 不能为空")
        team1 = await TravelTeamBuilder().create_team()
        team2 = await CompanyResearchTeamBuilder().create_team()

        all_teams = [team1, team2]
        for team in all_teams:
            # 保存 team
            team_comp = team.dump_component()
            comp = TeamComponent(**team_comp.model_dump())
            team2 = Team(
                    label=team_comp.label,
                    description=team_comp.description or "",
                    component=comp,
                )
            logger.info(f"create team for tenant: {message.tenant_id}, team: {team._team_id}")
            defaultModel = await self.gomtmapi.team_api.team_upsert(
                tenant=message.tenant_id,
                team=team._team_id,
                team2=team2,
            )
