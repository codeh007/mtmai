from autogen_agentchat.base import Team
from connecpy.context import ClientContext
from mtmai.clients.rest.api.ag_state_api import AgStateApi
from mtmai.clients.rest.api.chat_api import ChatApi
from mtmai.clients.rest.api.coms_api import ComsApi
from mtmai.clients.rest.api.model_api import ModelApi
from mtmai.clients.rest.api.resource_api import ResourceApi
from mtmai.clients.rest.api_client import ApiClient
from mtmai.clients.rest.configuration import Configuration
from mtmai.clients.rest.exceptions import NotFoundException
from mtmai.clients.rest.models.ag_state_upsert import AgStateUpsert
from mtmai.clients.rest.models.mt_component import MtComponent
from mtmai.mtlibs.id import generate_uuid
from mtmai.mtmpb.ag_connecpy import AsyncAgServiceClient

from .rest.models.state_type import StateType


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

    def ag_state_connect(self) -> AsyncAgServiceClient:
        if hasattr(self, "_ag_state_connect"):
            return self._ag_state_connect
        self._ag_state_connect = AsyncAgServiceClient(
            address=self.server_url,
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

    @property
    def resource_api(self):
        if hasattr(self, "_resource_api"):
            return self._resource_api
        self._resource_api = ResourceApi(self.api_client)
        return self._resource_api

    async def load_team_state(
        self,
        chat_id: str,
        tenant_id: str,
    ) -> Team:
        try:
            ag_state = await self.ag_state_api.ag_state_get(
                tenant=tenant_id,
                chat=chat_id,
            )
            return ag_state

        except NotFoundException:
            return None

    async def save_team_state(
        self, componentId: str, team: Team, tenant_id: str, chat_id: str
    ) -> None:
        # 确保停止团队的内部 agents
        if team and hasattr(team, "_participants"):
            for agent in team._participants:
                if hasattr(agent, "close"):
                    await agent.close()
        state = await team.save_state()
        await self.ag_state_api.ag_state_upsert(
            tenant=tenant_id,
            ag_state_upsert=AgStateUpsert(
                componentId=componentId,
                chatId=chat_id,
                state=state,
                type=StateType.TEAMSTATE,
            ),
        )

    # async def create_team(
    #     self,
    #     component_id_or_name: str | None = None,
    #     tid: str = None,
    # ):
    #     if not tid:
    #         tid = get_tenant_id()
    #     if not tid:
    #         raise ValueError("tenant_id is required")
    #     if not component_id_or_name:
    #         component_id_or_name = default_team_name
    #     model_client = await self.default_model_client(tid)

    #     resource_data = await self.resource_api.resource_get(
    #         tenant=tid,
    #         resource=component_id_or_name,
    #     )
    #     team_builder = resource_team_map.get(resource_data.type)
    #     if not team_builder:
    #         raise ValueError(
    #             f"cant create team for unsupported resource type: {resource_data.type}"
    #         )
    #     team = await team_builder.create_team(model_client)

    #     return team
    #     component_data: MtComponent = None
    #     # if is_uuid(component_id_or_name):
    #     component_data: MtComponent = None
    #     try:
    #         # TODO: 缓存优化
    #         component_data = await self.coms_api.coms_get(
    #             tenant=tid, com=component_id_or_name
    #         )
    #         # components = await self.coms_api.coms_list(tenant=tid,label=n)
    #         # component_data = components.rows[0]
    #         return Team.load_component(component_data.component)
    #     except NotFoundException:
    #         team = await team_builder_map.get(component_id_or_name).create_team(
    #             model_client
    #         )
    #         component_data = await self.upsert_team(
    #             tid,
    #             team,
    #         )
    #     if not component_data:
    #         raise ValueError("component_data is None")
    #     team = Team.load_component(component_data.component)
    #     return team
    #     # else:
    #     # team_builder = team_builder_map.get(component_id_or_name)
    #     # if not team_builder:
    #     #     raise ValueError(f"未找到团队构建器: {component_id_or_name}")
    #     # return await team_builder.create_team(model_client)

    #     # results = []
    #     # teams_list = await self.coms_api.coms_list(tenant=tid, label="default")
    #     # if teams_list.rows and len(teams_list.rows) > 0:
    #     #     logger.info(f"获取到默认聊天团队 {teams_list.rows[0].metadata.id}")
    #     #     results.append(teams_list.rows[0])

    #     # for team_builder in team_builders:
    #     #     label = team_builder.name
    #     #     logger.info(f"create team for tenant {tid}")

    #     #     team_comp = await team_builder.create_team(model_client)
    #     #     component_model = team_comp.dump_component()
    #     #     new_team = await self.coms_api.coms_upsert(
    #     #         tenant=tid,
    #     #         com=generate_uuid(),
    #     #         mt_component=MtComponent(
    #     #             label=label,
    #     #             description=component_model.description or "",
    #     #             componentType="team",
    #     #             component=component_model.model_dump(),
    #     #         ).model_dump(),
    #     #     )
    #     #     results.append(new_team)
    #     # return results

    # async def get_tenant_model_client(self, tid: str, model_name: str = "default"):
    #     # if hasattr(self, "_default_model_client"):
    #     #     return self._default_model_client
    #     defaultModel = await self.model_api.model_get(tenant=tid, model=model_name)
    #     model_dict = defaultModel.config.model_dump()
    #     model_dict.pop("n", None)
    #     return MtOpenAIChatCompletionClient(
    #         **model_dict,
    #     )

    async def upsert_team(
        self, tenant_id: str, team: Team, component_id: str | None = None
    ):
        team_comp = team.dump_component()
        return await self.coms_api.coms_upsert(
            tenant=tenant_id,
            com=component_id or generate_uuid(),
            mt_component=MtComponent(
                label=team.component_label,
                description=team.component_description,
                componentType=team.component_type,
                # version=team.component_version,
                component=team_comp.model_dump(),
            ).model_dump(),
        )
