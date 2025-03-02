from autogen_agentchat.base import Team
from loguru import logger
from mtmai.agents.model_client import MtmOpenAIChatCompletionClient
from mtmai.agents.team_builder.article_gen_teambuilder import ArticleGenTeamBuilder
from mtmai.agents.team_builder.assisant_team_builder import AssistantTeamBuilder
from mtmai.agents.team_builder.m1_web_builder import M1WebTeamBuilder
from mtmai.agents.team_builder.swram_team_builder import SwramTeamBuilder
from mtmai.agents.team_builder.travel_builder import TravelTeamBuilder
from mtmai.clients.rest.api.ag_state_api import AgStateApi
from mtmai.clients.rest.api.chat_api import ChatApi
from mtmai.clients.rest.api.coms_api import ComsApi
from mtmai.clients.rest.api_client import ApiClient
from mtmai.clients.rest.configuration import Configuration
from mtmai.clients.rest.models.ag_state_upsert import AgStateUpsert
from mtmai.clients.rest.models.chat_message_upsert import ChatMessageUpsert
from mtmai.clients.rest.models.mt_component import MtComponent
from mtmai.clients.rest_client import AsyncRestApi
from mtmai.mtlibs.id import generate_uuid


class AgClient:
    def __init__(
        self,
        server_url: str,
        access_token: str,
        # agService: ag_connecpy.AsyncAgServiceClient,
    ):
        self.server_url = server_url
        self.access_token = access_token
        # self.agService = agService
        self._ag_state_api = None
        self._api_client = None
        self._chat_api = None
        self._rest = None
        self._coms_api = None

    @property
    def api_client(self):
        if self._api_client is None:
            client_config = Configuration(
                host=self.config.server_url,
                access_token=self.config.token,
            )
            self._api_client = ApiClient(configuration=client_config)
        return self._api_client

    @property
    def ag_state_api(self):
        if self._ag_state_api is None:
            self._ag_state_api = AgStateApi(self.api_client)
        return self._ag_state_api

    @property
    def chat_api(self):
        if self._chat_api is None:
            self._chat_api = ChatApi(self.api_client)
        return self._chat_api

    @property
    def rest(self):
        if self._rest is None:
            self._rest = AsyncRestApi(
                self.config.server_url, self.config.token, self.config.tenant_id
            )

        return self._rest

    @property
    def coms_api(self):
        if self._coms_api is None:
            self._coms_api = ComsApi(self.api_client)
        return self._coms_api

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

    async def list_team_component(self, tenant_id: str):
        return await self.tenant_reset_teams(tenant_id)

    async def tenant_reset_teams(self, tenant_id: str):
        logger.info(f"TenantAgent 重置租户信息: {tenant_id}")
        results = []
        teams_list = await self.coms_api.coms_list(tenant=tenant_id, label="default")
        if teams_list.rows and len(teams_list.rows) > 0:
            logger.info(f"获取到默认聊天团队 {teams_list.rows[0].metadata.id}")
            results.append(teams_list.rows[0])
        defaultModel = await self.rest.model_api.model_get(
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
            new_team = await self.rest.coms_api.coms_upsert(
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

    async def handle_message_create(self, message: ChatMessageUpsert) -> None:
        await self.chat_api.chat_message_upsert(
            tenant=message.tenant_id,
            chat_message_upsert=message.model_dump(),
        )
