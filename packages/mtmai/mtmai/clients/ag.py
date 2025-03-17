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
from mtmai.clients.rest.models.ag_state_properties_state import AgStatePropertiesState
from mtmai.clients.rest.models.ag_state_upsert import AgStateUpsert
from mtmai.clients.rest.models.mt_component import MtComponent
from mtmai.clients.rest.models.state_type import StateType
from mtmai.mtlibs.id import generate_uuid
from mtmai.mtmpb.ag_connecpy import AsyncAgServiceClient


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
    ) -> dict:
        try:
            ag_state = await self.ag_state_api.ag_state_get(
                tenant=tenant_id,
                chat=chat_id,
            )
            if ag_state.state:
                if hasattr(ag_state.state, "actual_instance"):
                    return ag_state.state.actual_instance.model_dump()
            return ag_state.state.model_dump()
            # return ag_state.

        except NotFoundException:
            return None

    async def save_team_state(
        self, componentId: str, tenant_id: str, chat_id: str, state: dict
    ) -> None:
        await self.ag_state_api.ag_state_upsert(
            tenant=tenant_id,
            ag_state_upsert=AgStateUpsert(
                componentId=componentId,
                chatId=chat_id,
                state=AgStatePropertiesState().from_dict(state),
                type=StateType.TEAMSTATE,
            ),
        )

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
