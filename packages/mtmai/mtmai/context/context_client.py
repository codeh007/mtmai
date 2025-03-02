from contextvars import ContextVar

from ..clients.ag import AgClient

tenant_id_context: ContextVar[str] = ContextVar("user_tenant_id", default=None)


def get_tenant_id() -> str:
    return tenant_id_context.get()


def set_tenant_id(tenant_id: str):
    tenant_id_context.set(tenant_id)


step_run_id_context: ContextVar[str] = ContextVar("step_run_id", default=None)


def get_step_run_id() -> str:
    return step_run_id_context.get()


def set_step_run_id(step_run_id: str):
    step_run_id_context.set(step_run_id)


run_id_context: ContextVar[str] = ContextVar("run_id", default=None)


def get_run_id() -> str:
    return run_id_context.get()


def set_run_id(run_id: str):
    run_id_context.set(run_id)


server_url_context: ContextVar[str] = ContextVar("server_url", default=None)


def get_server_url() -> str:
    return server_url_context.get()


def set_server_url_ctx(server_url: str):
    server_url_context.set(server_url)


access_token_context: ContextVar[str] = ContextVar("access_token", default=None)


def get_access_token() -> str:
    return access_token_context.get()


def set_access_token_ctx(access_token: str):
    access_token_context.set(access_token)


class TenantClient:
    def __init__(self):
        self.tenant_id = get_tenant_id()
        self.run_id = get_run_id()
        self.step_run_id = get_step_run_id()

        server_url = get_server_url()
        if server_url is None:
            raise ValueError("server_url context is not set")
        access_token = get_access_token()
        if access_token is None:
            raise ValueError("access_token context is not set")

        self.ag: AgClient = AgClient(server_url, access_token)

    def show_info(self):
        print(
            f"(TenantClient) tenant_id: {self.tenant_id}, run_id: {self.run_id}, step_run_id: {self.step_run_id}"
        )
