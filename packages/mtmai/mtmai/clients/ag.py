import json

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
from mtmai.clients.rest.api.chat_api import ChatApi
from mtmai.clients.rest.api.coms_api import ComsApi
from mtmai.clients.rest.api.model_api import ModelApi
from mtmai.clients.rest.api_client import ApiClient
from mtmai.clients.rest.configuration import Configuration
from mtmai.clients.rest.models.chat_message_upsert import ChatMessageUpsert
from mtmai.clients.rest.models.mt_component import MtComponent
from mtmai.mtlibs.id import generate_uuid
from mtmai.mtmpb.ag_connecpy import AsyncAgServiceClient

from ..mtmpb.ag_pb2 import AgState

# from .rest.models.ag_state import AgState


class AgClient:
    def __init__(
        self,
        server_url: str,
        access_token: str,
    ):
        self.server_url = server_url
        self.access_token = access_token
        self.client_context = ClientContext(
            headers={
                "Authorization": f"Bearer {access_token}",
                # "X-Tid": tenant_id,
            }
        )
        self.client_config = Configuration(
            host=self.server_url,
            access_token=self.access_token,
        )

    @property
    def api_client(self):
        if hasattr(self, "_api_client"):
            return self._api_client
        self._api_client = ApiClient(configuration=self.client_config)
        return self._api_client

    @property
    def ag_state_api(self):
        if hasattr(self, "_ag_state_api"):
            return self._ag_state_api
        self._ag_state_api = AgStateApi(self.api_client)
        return self._ag_state_api

    def ag_state_connect(self):
        if hasattr(self, "_ag_state_connect"):
            return self._ag_state_connect
        self._ag_state_connect = AsyncAgServiceClient(
            address=self.server_url,
            # session=self.api_client.session,
        )
        return self._ag_state_connect

    @property
    def chat_api(self):
        if hasattr(self, "_chat_api"):
            return self._chat_api
        self._chat_api = ChatApi(self.api_client)
        return self._chat_api

    @property
    def model_api(self):
        if hasattr(self, "_model_api"):
            return self._model_api
        self._model_api = ModelApi(self.api_client)
        return self._model_api

    @property
    def coms_api(self):
        if hasattr(self, "_coms_api"):
            return self._coms_api
        self._coms_api = ComsApi(self.api_client)
        return self._coms_api

    async def load_team_state(
        self,
        session_id: str,
        tenant_id: str,
    ) -> Team:
        team_state = await self.ag_state_api.ag_state_get(
            tenant=tenant_id,
            componentId=session_id,
        )
        return Team.load_state(team_state.state)

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
        # await self.ag_state_api.ag_state_upsert(
        #     tenant=tenant_id,
        #     ag_state_upsert=AgStateUpsert(
        #         componentId=team_id,
        #         runId=run_id,
        #         state=state,
        #     ).model_dump(),
        # )
        await self.ag_state_connect().SetState(
            ctx=self.client_context,
            request=AgState(
                # tenant=tenant_id,
                component_id=team_id,
                run_id=run_id,
                state=json.dumps(state),
            ),
        )

    async def list_team_component(self, tenant_id: str):
        return await self.tenant_reset_teams(tenant_id)

    async def tenant_reset_teams(self, tid: str):
        logger.info(f"TenantAgent 重置租户信息: {tid}")
        results = []
        teams_list = await self.coms_api.coms_list(tenant=tid, label="default")
        if teams_list.rows and len(teams_list.rows) > 0:
            logger.info(f"获取到默认聊天团队 {teams_list.rows[0].metadata.id}")
            results.append(teams_list.rows[0])

        model_client = await self.get_default_model_client(tid)
        self.team_builders = [
            AssistantTeamBuilder(),
            SwramTeamBuilder(),
            ArticleGenTeamBuilder(),
            M1WebTeamBuilder(),
            TravelTeamBuilder(),
        ]
        for team_builder in self.team_builders:
            label = team_builder.name
            logger.info(f"create team for tenant {tid}")

            team_comp = await team_builder.create_team(model_client)
            component_model = team_comp.dump_component()
            new_team = await self.coms_api.coms_upsert(
                tenant=tid,
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

    async def get_component(self, tenant_id: str, component_id: str):
        return await self.coms_api.coms_get(
            tenant=tenant_id,
            com=component_id,
        )

    async def get_team(self, tenant_id: str, team_id: str):
        team_comp_data = await self.coms_api.coms_get(
            tenant=tenant_id,
            com=team_id,
        )
        team = Team.load_component(team_comp_data.component)
        return team

    async def get_default_model_client(self, tid: str):
        defaultModel = await self.model_api.model_get(tenant=tid, model="default")
        model_dict = defaultModel.config.model_dump()
        model_dict.pop("n", None)
        return MtmOpenAIChatCompletionClient(
            **model_dict,
        )
