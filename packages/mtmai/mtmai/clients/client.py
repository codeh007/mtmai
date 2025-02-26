import asyncio
from logging import Logger
from typing import Callable

import httpx
from connecpy.context import ClientContext
from mtmai.clients.admin import AdminClient, new_admin
from mtmai.clients.events import EventClient
from mtmai.clients.rest_client import RestApi
from mtmai.loader import ClientConfig, ConfigLoader
from mtmai.mtmpb import ag_connecpy, events_connecpy, mtm_connecpy
from mtmai.run_event_listener import RunEventListenerClient
from mtmai.worker.dispatcher.dispatcher import DispatcherClient, new_dispatcher
from mtmai.workflow_listener import PooledWorkflowRunListener


class Client:
    admin: AdminClient
    dispatcher: DispatcherClient
    event: EventClient
    rest: RestApi
    workflow_listener: PooledWorkflowRunListener
    logInterceptor: Logger
    debug: bool = False

    @classmethod
    def from_environment(
        cls,
        defaults: ClientConfig = ClientConfig(),
        debug: bool = False,
        *opts_functions: Callable[[ClientConfig], None],
    ):
        try:
            loop = asyncio.get_running_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)

        config: ClientConfig = ConfigLoader(".").load_client_config(defaults)
        for opt_function in opts_functions:
            opt_function(config)

        return cls.from_config(config, debug)

    @classmethod
    def from_config(
        cls,
        config: ClientConfig = ClientConfig(),
        debug: bool = False,
    ):
        try:
            loop = asyncio.get_running_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)

        if config.tls_config is None:
            raise ValueError("TLS config is required")

        if config.host_port is None:
            raise ValueError("Host and port are required")

        eventsService = events_connecpy.AsyncEventsServiceClient(
            config.server_url,
            timeout=20,
        )
        event_client = EventClient(config, eventsService)
        admin_client = new_admin(config)
        dispatcher_client = new_dispatcher(config)
        rest_client = RestApi(config.server_url, config.token, config.tenant_id)
        workflow_listener = None  # Initialize this if needed

        return cls(
            event_client,
            admin_client,
            dispatcher_client,
            workflow_listener,
            rest_client,
            config,
            debug,
        )

    def __init__(
        self,
        event_client: EventClient,
        admin_client: AdminClient,
        dispatcher_client: DispatcherClient,
        workflow_listener: PooledWorkflowRunListener,
        rest_client: RestApi,
        config: ClientConfig,
        debug: bool = False,
    ):
        try:
            loop = asyncio.get_running_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)

        self.admin = admin_client
        self.dispatcher = dispatcher_client
        self.event = event_client
        self.rest = rest_client
        self.config = config
        self.listener = RunEventListenerClient(config)
        self.workflow_listener = workflow_listener
        self.logInterceptor = config.logInterceptor
        self.debug = debug

        self.default_client_timeout = 20
        # MTM 客户端
        # 参考: https://github.com/i2y/connecpy/blob/main/example/async_client.py

        self.client_context = ClientContext(
            headers={
                "Authorization": f"Bearer {config.token}",
                "X-Tid": config.tenant_id,
            }
        )
        gomtm_api_path_prefix = "/mtmapi"
        gomtm_api_url = config.server_url + gomtm_api_path_prefix
        self.session = httpx.AsyncClient(
            base_url=gomtm_api_url,
            timeout=self.default_client_timeout,
        )
        self.ag = ag_connecpy.AsyncAgServiceClient(
            gomtm_api_url, session=self.session, timeout=self.default_client_timeout
        )
        self.events = events_connecpy.AsyncEventsServiceClient(
            gomtm_api_url, session=self.session, timeout=self.default_client_timeout
        )
        self.mtm = mtm_connecpy.AsyncMtmServiceClient(
            gomtm_api_url, session=self.session, timeout=self.default_client_timeout
        )


def with_host_port(host: str, port: int):
    def with_host_port_impl(config: ClientConfig):
        config.host = host
        config.port = port

    return with_host_port_impl


# def get_gomtm():
#     backend_url = get_backend_url()
#     if not backend_url:
#         raise ValueError("backend_url is required")
#     api_token = get_api_token_context()
#     tenant_id = get_tenant_id()
#     return AsyncRestApi(backend_url, api_token, tenant_id)


# gomtm_ctx: ContextVar["AsyncRestApi"] = ContextVar("gomtm_api_ctx", default=None)


# def get_gomtm_api_context() -> AsyncRestApi:
#     a = gomtm_ctx.get()
#     return a


# def set_gomtm_api_context(gomtm_api: AsyncRestApi):
#     gomtm_ctx.set(gomtm_api)
