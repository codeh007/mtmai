from contextvars import ContextVar

META_RUN_BY_TENANT = "runByTenantId"
META_SESSION_ID = "sessionId"
META_RUN_BY_USER_ID = "runByUserId"

tenant_id_context: ContextVar[str] = ContextVar("user_tenant_id", default=None)


def get_tenant_id() -> str:
    return tenant_id_context.get()


def set_tenant_id(tenant_id: str):
    tenant_id_context.set(tenant_id)


user_id_context: ContextVar[str] = ContextVar("user_id", default=None)


def get_current_user_id() -> str:
    return user_id_context.get()


def set_current_user_id(user_id: str):
    user_id_context.set(user_id)


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


chat_session_id_ctx: ContextVar[str] = ContextVar("chat_session_id", default=None)


def get_chat_session_id_ctx() -> str:
    return chat_session_id_ctx.get()


def set_chat_session_id_ctx(chat_session_id: str):
    chat_session_id_ctx.set(chat_session_id)


run_by_user_id_ctx: ContextVar[str] = ContextVar("run_by_user_id", default=None)


def get_run_by_user_id_ctx() -> str:
    return run_by_user_id_ctx.get()


def set_run_by_user_id_ctx(run_by_user_id: str):
    run_by_user_id_ctx.set(run_by_user_id)


team_id_ctx: ContextVar[str] = ContextVar("team_id", default=None)


def get_team_id_ctx() -> str:
    return team_id_ctx.get()


def set_team_id_ctx(team_id: str):
    team_id_ctx.set(team_id)


step_canceled_ctx: ContextVar[bool] = ContextVar("step_canceled_ctx", default=False)


def get_step_canceled_ctx() -> str:
    return step_canceled_ctx.get()


def set_step_canceled_ctx(step_canceled: str):
    step_canceled_ctx.set(step_canceled)
