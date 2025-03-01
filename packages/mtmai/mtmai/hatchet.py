from typing import Any, Callable, List, Optional, Type, TypeVar, Union

from autogen_core import AgentRuntime
from connecpy.context import ClientContext
from loguru import logger
from pydantic import BaseModel

import mtmai.mtmpb.mtm_pb2 as _pb2
from mtmai.clients.admin import AdminClient
from mtmai.clients.client import Client
from mtmai.clients.events import EventClient
from mtmai.context.context import Context
from mtmai.core import loader
from mtmai.core.config import settings
from mtmai.core.loader import ClientConfig, ConfigLoader, CredentialsData
from mtmai.features.cron import CronClient
from mtmai.features.scheduled import ScheduledClient
from mtmai.models._types import DesiredWorkerLabel, RateLimit
from mtmai.mtlibs.callable import ConcurrencyFunction, HatchetCallable
from mtmai.mtmpb.mtm_connecpy import AsyncMtmServiceClient
from mtmai.mtmpb.workflows_pb2 import (
    ConcurrencyLimitStrategy,
    CreateStepRateLimit,
    DesiredWorkerLabels,
    StickyStrategy,
)
from mtmai.run_event_listener import RunEventListenerClient
from mtmai.worker.dispatcher.dispatcher import DispatcherClient
from mtmai.worker.worker import Worker, register_on_worker
from mtmai.workflow import ConcurrencyExpression, WorkflowMeta

from .clients.agent_runtime.mtm_runtime import MtmAgentRuntime
from .clients.rest_client import AsyncRestApi

T = TypeVar("T", bound=BaseModel)
TWorkflow = TypeVar("TWorkflow", bound=object)


def workflow(
    name: str = "",
    on_events: list[str] | None = None,
    on_crons: list[str] | None = None,
    version: str = "",
    timeout: str = "60m",
    schedule_timeout: str = "5m",
    sticky: Union[StickyStrategy.Value, None] = None,  # type: ignore[name-defined]
    default_priority: int | None = None,
    concurrency: ConcurrencyExpression | None = None,
    input_validator: Type[T] | None = None,
) -> Callable[[Type[TWorkflow]], WorkflowMeta]:
    on_events = on_events or []
    on_crons = on_crons or []

    def inner(cls: Type[TWorkflow]) -> WorkflowMeta:
        nonlocal name
        name = name or str(cls.__name__)

        setattr(cls, "on_events", on_events)
        setattr(cls, "on_crons", on_crons)
        setattr(cls, "name", name)
        setattr(cls, "version", version)
        setattr(cls, "timeout", timeout)
        setattr(cls, "schedule_timeout", schedule_timeout)
        setattr(cls, "sticky", sticky)
        setattr(cls, "default_priority", default_priority)
        setattr(cls, "concurrency_expression", concurrency)

        # Define a new class with the same name and bases as the original, but
        # with WorkflowMeta as its metaclass

        ## TODO: Figure out how to type this metaclass correctly
        setattr(cls, "input_validator", input_validator)

        return WorkflowMeta(name, cls.__bases__, dict(cls.__dict__))

    return inner


def step(
    name: str = "",
    timeout: str = "",
    parents: list[str] | None = None,
    retries: int = 0,
    rate_limits: list[RateLimit] | None = None,
    desired_worker_labels: dict[str, DesiredWorkerLabel] = {},
    backoff_factor: float | None = None,
    backoff_max_seconds: int | None = None,
) -> Callable[..., Any]:
    parents = parents or []

    def inner(func: Callable[[Context], Any]) -> Callable[[Context], Any]:
        limits = None
        if rate_limits:
            limits = [rate_limit._req for rate_limit in rate_limits or []]

        setattr(func, "_step_name", name.lower() or str(func.__name__).lower())
        setattr(func, "_step_parents", parents)
        setattr(func, "_step_timeout", timeout)
        setattr(func, "_step_retries", retries)
        setattr(func, "_step_rate_limits", retries)
        setattr(func, "_step_rate_limits", limits)
        setattr(func, "_step_backoff_factor", backoff_factor)
        setattr(func, "_step_backoff_max_seconds", backoff_max_seconds)

        def create_label(d: DesiredWorkerLabel) -> DesiredWorkerLabels:
            value = d["value"] if "value" in d else None
            return DesiredWorkerLabels(
                strValue=str(value) if not isinstance(value, int) else None,
                intValue=value if isinstance(value, int) else None,
                required=d["required"] if "required" in d else None,  # type: ignore[arg-type]
                weight=d["weight"] if "weight" in d else None,
                comparator=d["comparator"] if "comparator" in d else None,  # type: ignore[arg-type]
            )

        setattr(
            func,
            "_step_desired_worker_labels",
            {key: create_label(d) for key, d in desired_worker_labels.items()},
        )

        return func

    return inner


def on_failure_step(
    name: str = "",
    timeout: str = "",
    retries: int = 0,
    rate_limits: list[RateLimit] | None = None,
    backoff_factor: float | None = None,
    backoff_max_seconds: int | None = None,
) -> Callable[..., Any]:
    def inner(func: Callable[[Context], Any]) -> Callable[[Context], Any]:
        limits = None
        if rate_limits:
            limits = [
                CreateStepRateLimit(key=rate_limit.static_key, units=rate_limit.units)  # type: ignore[arg-type]
                for rate_limit in rate_limits or []
            ]

        setattr(
            func, "_on_failure_step_name", name.lower() or str(func.__name__).lower()
        )
        setattr(func, "_on_failure_step_timeout", timeout)
        setattr(func, "_on_failure_step_retries", retries)
        setattr(func, "_on_failure_step_rate_limits", limits)
        setattr(func, "_on_failure_step_backoff_factor", backoff_factor)
        setattr(func, "_on_failure_step_backoff_max_seconds", backoff_max_seconds)

        return func

    return inner


def function(
    name: str = "",
    auto_register: bool = True,
    on_events: list | None = None,
    on_crons: list | None = None,
    version: str = "",
    timeout: str = "60m",
    schedule_timeout: str = "5m",
    sticky: StickyStrategy = None,
    retries: int = 0,
    rate_limits: List[RateLimit] | None = None,
    desired_worker_labels: dict[str:DesiredWorkerLabel] = {},
    concurrency: ConcurrencyFunction | None = None,
    on_failure: Optional["HatchetCallable"] = None,
    default_priority: int | None = None,
):
    def inner(func: Callable[[Context], T]) -> HatchetCallable[T]:
        return HatchetCallable(
            func=func,
            name=name,
            auto_register=auto_register,
            on_events=on_events,
            on_crons=on_crons,
            version=version,
            timeout=timeout,
            schedule_timeout=schedule_timeout,
            sticky=sticky,
            retries=retries,
            rate_limits=rate_limits,
            desired_worker_labels=desired_worker_labels,
            concurrency=concurrency,
            on_failure=on_failure,
            default_priority=default_priority,
        )

    return inner


def durable(
    name: str = "",
    auto_register: bool = True,
    on_events: list | None = None,
    on_crons: list | None = None,
    version: str = "",
    timeout: str = "60m",
    schedule_timeout: str = "5m",
    sticky: StickyStrategy = None,
    retries: int = 0,
    rate_limits: List[RateLimit] | None = None,
    desired_worker_labels: dict[str:DesiredWorkerLabel] = {},
    concurrency: ConcurrencyFunction | None = None,
    on_failure: HatchetCallable | None = None,
    default_priority: int | None = None,
):
    def inner(func: HatchetCallable) -> HatchetCallable:
        func.durable = True

        f = function(
            name=name,
            auto_register=auto_register,
            on_events=on_events,
            on_crons=on_crons,
            version=version,
            timeout=timeout,
            schedule_timeout=schedule_timeout,
            sticky=sticky,
            retries=retries,
            rate_limits=rate_limits,
            desired_worker_labels=desired_worker_labels,
            concurrency=concurrency,
            on_failure=on_failure,
            default_priority=default_priority,
        )

        resp = f(func)
        resp.durable = True
        return resp

    return inner


def concurrency(
    name: str = "concurrency",
    max_runs: int = 1,
    limit_strategy: ConcurrencyLimitStrategy = ConcurrencyLimitStrategy.GROUP_ROUND_ROBIN,
):
    def inner(func: Callable[[Context], str]) -> ConcurrencyFunction:
        return ConcurrencyFunction(func, name, max_runs, limit_strategy)

    return inner


class Hatchet:
    _client: Client
    cron: CronClient
    scheduled: ScheduledClient
    functions: List[HatchetCallable] = []

    def __init__(
        self,
        debug: bool = False,
        client: Optional[Client] = None,
    ):
        if client is not None:
            self._client = client
        else:
            config = ClientConfig(
                server_url=settings.GOMTM_URL,
                # 绑定 python 默认logger,这样,就可以不用依赖 hatchet 内置的ctx.log()
                # logger=logger,
            )
            client_config = loader.ConfigLoader().load_client_config(config)
            self._client = Client.from_config(client_config, debug=debug)
        self.cron = CronClient(self._client)
        self.scheduled = ScheduledClient(self._client)
        self.debug = debug
        self._agent_runtime: AgentRuntime | None = None

    @property
    def admin(self) -> AdminClient:
        return self._client.admin

    @property
    def dispatcher(self) -> DispatcherClient:
        return self._client.dispatcher

    @property
    def event(self) -> EventClient:
        return self._client.event

    @property
    def rest(self) -> AsyncRestApi:
        return self._client.rest

    @property
    def mtm(self) -> AsyncMtmServiceClient:
        return self._client.mtm

    @property
    def listener(self) -> RunEventListenerClient:
        return self._client.listener

    @property
    def config(self) -> ClientConfig:
        return self._client.config

    @property
    def tenant_id(self) -> str:
        return self._client.config.tenant_id

    @property
    def agent_runtime(self):
        if self._agent_runtime is None:
            self._agent_runtime = MtmAgentRuntime(config=self._client.config)
        return self._agent_runtime

    workflow = staticmethod(workflow)

    step = staticmethod(step)

    on_failure_step = staticmethod(on_failure_step)

    async def boot(self):
        if not self._client.config.token:
            if (
                not self._client.config.credentials
                or not self._client.config.credentials.username
                or not self._client.config.credentials.password
            ):
                logger.info("login required")
                email = input("email:")
                password = input("password:")
                # self.config.token = f"{email}:{password}"
                self.config.credentials = CredentialsData(
                    username=email, password=password
                )
            resp = await self.mtm.Login(
                ctx=ClientContext(),
                request=_pb2.LoginReq(
                    username=self.config.credentials.username,
                    password=self.config.credentials.password,
                ),
            )
            if not resp.access_token:
                raise ValueError("credentials invalid")
            self.config.token = resp.access_token
            self.config.credentials.token = resp.access_token
            await ConfigLoader.save_credentials(self.config.credentials)

        self._client = Client.from_config(self.config, debug=self.debug)
        self.config.tenant_id = await self.load_default_tenant()
        self._client = Client.from_config(self.config, debug=self.debug)

    async def load_default_tenant(self):
        resp = await self._client.rest.user_api.tenant_memberships_list()
        return resp.rows[0].tenant.metadata.id

    def function(
        self,
        name: str = "",
        auto_register: bool = True,
        on_events: list | None = None,
        on_crons: list | None = None,
        version: str = "",
        timeout: str = "60m",
        schedule_timeout: str = "5m",
        retries: int = 0,
        rate_limits: List[RateLimit] | None = None,
        desired_worker_labels: dict[str:DesiredWorkerLabel] = {},
        concurrency: ConcurrencyFunction | None = None,
        on_failure: Optional["HatchetCallable"] = None,
        default_priority: int | None = None,
    ):
        resp = function(
            name=name,
            auto_register=auto_register,
            on_events=on_events,
            on_crons=on_crons,
            version=version,
            timeout=timeout,
            schedule_timeout=schedule_timeout,
            retries=retries,
            rate_limits=rate_limits,
            desired_worker_labels=desired_worker_labels,
            concurrency=concurrency,
            on_failure=on_failure,
            default_priority=default_priority,
        )

        def wrapper(func: Callable[[Context], T]) -> HatchetCallable[T]:
            wrapped_resp = resp(func)

            if wrapped_resp.function_auto_register:
                self.functions.append(wrapped_resp)

            wrapped_resp.with_namespace(self._client.config.namespace)

            return wrapped_resp

        return wrapper

    def durable(
        self,
        name: str = "",
        auto_register: bool = True,
        on_events: list | None = None,
        on_crons: list | None = None,
        version: str = "",
        timeout: str = "60m",
        schedule_timeout: str = "5m",
        sticky: StickyStrategy = None,
        retries: int = 0,
        rate_limits: List[RateLimit] | None = None,
        desired_worker_labels: dict[str:DesiredWorkerLabel] = {},
        concurrency: ConcurrencyFunction | None = None,
        on_failure: Optional["HatchetCallable"] = None,
        default_priority: int | None = None,
    ) -> Callable[[HatchetCallable], HatchetCallable]:
        resp = durable(
            name=name,
            auto_register=auto_register,
            on_events=on_events,
            on_crons=on_crons,
            version=version,
            timeout=timeout,
            schedule_timeout=schedule_timeout,
            sticky=sticky,
            retries=retries,
            rate_limits=rate_limits,
            desired_worker_labels=desired_worker_labels,
            concurrency=concurrency,
            on_failure=on_failure,
            default_priority=default_priority,
        )

        def wrapper(func: Callable[[Context], T]) -> HatchetCallable[T]:
            wrapped_resp = resp(func)

            if wrapped_resp.function_auto_register:
                self.functions.append(wrapped_resp)

            wrapped_resp.with_namespace(self._client.config.namespace)

            return wrapped_resp

        return wrapper

    def worker(
        self, name: str, max_runs: int | None = None, labels: dict[str, str | int] = {}
    ):
        worker = Worker(
            name=name,
            max_runs=max_runs,
            labels=labels,
            config=self._client.config,
            debug=self._client.debug,
        )

        for func in self.functions:
            register_on_worker(func, worker)

        return worker
