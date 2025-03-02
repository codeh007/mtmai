import asyncio
from logging import Logger

import httpx
from connecpy.context import ClientContext
from mtmai.clients.admin import AdminClient, new_admin
from mtmai.clients.events import EventClient
from mtmai.clients.rest_client import AsyncRestApi
from mtmai.core.config import settings
from mtmai.core.loader import ClientConfig
from mtmai.mtmpb import ag_connecpy, events_connecpy, mtm_connecpy
from mtmai.run_event_listener import RunEventListenerClient
from mtmai.worker.dispatcher.dispatcher import DispatcherClient, new_dispatcher
from mtmai.workflow_listener import PooledWorkflowRunListener


class Client:
    admin: AdminClient
    dispatcher: DispatcherClient
    event: EventClient
    rest: AsyncRestApi
    workflow_listener: PooledWorkflowRunListener
    logInterceptor: Logger
    debug: bool = False

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

        # eventsService = events_connecpy.AsyncEventsServiceClient(
        #     config.server_url,
        #     timeout=20,
        # )
        event_client = EventClient(
            server_url=config.server_url,
            token=config.token,
            tenant_id=config.tenant_id,
            namespace=config.namespace,
        )
        admin_client = new_admin(config)
        dispatcher_client = new_dispatcher(config)
        rest_client = AsyncRestApi(config.server_url, config.token, config.tenant_id)
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
        rest_client: AsyncRestApi,
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

        # MTM 客户端
        # 参考: https://github.com/i2y/connecpy/blob/main/example/async_client.py

        self.client_context = ClientContext(
            headers={
                "Authorization": f"Bearer {config.token}",
                "X-Tid": config.tenant_id,
            }
        )
        gomtm_api_url = config.server_url + settings.GOMTM_API_PATH_PREFIX
        self.session = httpx.AsyncClient(
            base_url=gomtm_api_url,
            timeout=settings.DEFAULT_CLIENT_TIMEOUT,
        )
        self.ag = ag_connecpy.AsyncAgServiceClient(
            gomtm_api_url, session=self.session, timeout=settings.DEFAULT_CLIENT_TIMEOUT
        )
        self.events = events_connecpy.AsyncEventsServiceClient(
            gomtm_api_url, session=self.session, timeout=settings.DEFAULT_CLIENT_TIMEOUT
        )
        self.mtm = mtm_connecpy.AsyncMtmServiceClient(
            gomtm_api_url, session=self.session, timeout=settings.DEFAULT_CLIENT_TIMEOUT
        )
