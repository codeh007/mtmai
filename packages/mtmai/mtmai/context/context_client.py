from typing import Any

from autogen_ext.tools.mcp import SseServerParams
from mtmai.clients.ag import AgClient
from mtmai.clients.events import EventClient
from mtmai.context.ctx import (
    META_RUN_BY_TENANT,
    META_RUN_BY_USER_ID,
    META_SESSION_ID,
    get_access_token,
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
        self.run_id = get_run_id()
        self.step_run_id = get_step_run_id()

        self.server_url = get_server_url()
        if self.server_url is None:
            raise ValueError("server_url context is not set")
        self.access_token = get_access_token()
        if self.access_token is None:
            raise ValueError("access_token context is not set")

    @property
    def ag(self) -> AgClient:
        if hasattr(self, "_ag"):
            return self._ag
        self._ag = AgClient(get_server_url(), get_access_token())
        return self._ag

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
