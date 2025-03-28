from typing import Any

from autogen_ext.tools.mcp import SseServerParams
from clients.rest.api.platform_account_api import PlatformAccountApi
from clients.rest.api.resource_api import ResourceApi
from clients.rest.api_client import ApiClient
from clients.rest.configuration import Configuration
from mtmai.clients.ag import AgClient
from mtmai.clients.events import EventClient
from mtmai.context.ctx import (
    META_RUN_BY_TENANT,
    META_RUN_BY_USER_ID,
    META_SESSION_ID,
    get_access_token,
    get_chat_session_id_ctx,
    get_run_id,
    get_server_url,
    get_step_run_id,
    get_tenant_id,
    set_chat_session_id_ctx,
    set_run_by_user_id_ctx,
    set_run_id,
    set_step_run_id,
    set_tenant_id,
)
from mtmai.worker.dispatcher.action_listener import Action


def parser_ctx_from_metas(meta: dict[str, str]):
    if META_RUN_BY_TENANT in meta:
        set_tenant_id(meta[META_RUN_BY_TENANT])
    if META_SESSION_ID in meta:
        set_chat_session_id_ctx(meta[META_SESSION_ID])
    if META_RUN_BY_USER_ID in meta:
        set_run_by_user_id_ctx(meta[META_RUN_BY_USER_ID])


def parse_ctx_from_action(action: Action):
    set_run_id(action.workflow_run_id)
    set_step_run_id(action.step_run_id)
    parser_ctx_from_metas(action.additional_metadata)


class TenantClient:
    def __init__(self):
        self.tenant_id = get_tenant_id()
        assert self.tenant_id is not None
        self.run_id = get_run_id()
        self.step_run_id = get_step_run_id()
        self.session_id = get_chat_session_id_ctx()
        self.server_url = get_server_url()
        if self.server_url is None:
            raise ValueError("server_url context is not set")
        self.access_token = get_access_token()
        if self.access_token is None:
            raise ValueError("access_token context is not set")

        # self.server_url = server_url
        # self.access_token = access_token
        # self.client_context = ClientContext(
        #     headers={
        #         "Authorization": f"Bearer {access_token}",
        #     }
        # )
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
    def ag(self) -> AgClient:
        if hasattr(self, "_ag"):
            return self._ag
        self._ag = AgClient(get_server_url(), get_access_token())
        return self._ag

    @property
    def platform_account_api(self):
        if hasattr(self, "_platform_account_api"):
            return self._platform_account_api
        self._platform_account_api = PlatformAccountApi(self.api_client)
        return self._platform_account_api

    @property
    def resource_api(self):
        if hasattr(self, "_resource_api"):
            return self._resource_api
        self._resource_api = ResourceApi(self.api_client)
        return self._resource_api

    @property
    def event(self) -> EventClient:
        if hasattr(self, "_event"):
            return self._event
        self._event = EventClient(get_server_url(), get_access_token())
        return self._event

    async def emit(self, event: Any):
        await self.event.emit(event)

    async def get_mcp_endpoint(self):
        server_params = SseServerParams(
            url="http://localhost:8383/mcp/sse",
            headers={"Authorization": "Bearer token"},
        )
        return server_params
