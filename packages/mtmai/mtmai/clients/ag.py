from autogen_agentchat.base import Team
from connecpy.context import ClientContext
from loguru import logger
from mtmai.agents.model_client import MtmOpenAIChatCompletionClient
from mtmai.agents.team_builder.article_gen_teambuilder import ArticleGenTeamBuilder
from mtmai.agents.team_builder.assisant_team_builder import AssistantTeamBuilder
from mtmai.agents.team_builder.m1_web_builder import M1WebTeamBuilder
from mtmai.agents.team_builder.swram_team_builder import SwramTeamBuilder
from mtmai.agents.team_builder.travel_builder import TravelTeamBuilder
from mtmai.clients.rest.api.ag_state_api import AgStateApi
from mtmai.clients.rest.api_client import ApiClient
from mtmai.clients.rest.models.ag_state_upsert import AgStateUpsert
from mtmai.clients.rest.models.mt_component import MtComponent
from mtmai.loader import ClientConfig
from mtmai.mtlibs.id import generate_uuid
from mtmai.mtmpb import ag_connecpy


class AgClient:
    def __init__(
        self, config: ClientConfig, agService: ag_connecpy.AsyncAgServiceClient
    ):
        self.client_context = ClientContext(
            headers={
                "Authorization": f"Bearer {config.token}",
                "X-Tid": config.tenant_id,
            }
        )
        self.agService = agService
        self._ag_state_api = None
        self._api_client = None

    @property
    def api_client(self):
        if self._api_client is None:
            self._api_client = ApiClient(configuration=self.config)
        return self._api_client

    @property
    def ag_state_api(self):
        if self._ag_state_api is None:
            self._ag_state_api = AgStateApi(self.api_client)
        return self._ag_state_api

    async def save_team_state(
        self, team: Team, team_id: str, tenant_id: str, run_id: str
    ) -> None:
        """保存团队状态"""
        logger.info("保存团队状态")
        # 确保停止团队的内部 agents
        if team and hasattr(team, "_participants"):
            for agent in team._participants:
                if hasattr(agent, "close"):
                    await agent.close()
        state = await team.save_state()
        await self.ag_state_api.ag_state_upsert(
            tenant=tenant_id,
            ag_state_upsert=AgStateUpsert(
                componentId=team_id,
                runId=run_id,
                state=state,
            ).model_dump(),
        )

    async def tenant_reset_teams(self, tenant_id: str):
        logger.info(f"TenantAgent 重置租户信息: {tenant_id}")
        results = []
        teams_list = await self.hatctx.aio.rest_client.aio.coms_api.coms_list(
            tenant=tenant_id, label="default"
        )
        if teams_list.rows and len(teams_list.rows) > 0:
            logger.info(f"获取到默认聊天团队 {teams_list.rows[0].metadata.id}")
            results.append(teams_list.rows[0])
        defaultModel = await self.hatctx.aio.rest_client.aio.model_api.model_get(
            tenant=tenant_id, model="default"
        )
        model_dict = defaultModel.config.model_dump()
        model_dict.pop("n", None)
        model_client = MtmOpenAIChatCompletionClient(
            **model_dict,
        )

        self.team_builders = [
            AssistantTeamBuilder(),
            SwramTeamBuilder(),
            ArticleGenTeamBuilder(),
            M1WebTeamBuilder(),
            TravelTeamBuilder(),
        ]
        for team_builder in self.team_builders:
            label = team_builder.name
            logger.info(f"create team for tenant {tenant_id}")
            team_comp = await team_builder.create_team(model_client)
            component_model = team_comp.dump_component()
            new_team = await self.hatctx.aio.rest_client.aio.coms_api.coms_upsert(
                tenant=tenant_id,
                com=generate_uuid(),
                mt_component=MtComponent(
                    label=label,
                    description=component_model.description or "",
                    componentType="team",
                    component=component_model.model_dump(),
                ).model_dump(),
            )
            results.append(new_team)
        return results
