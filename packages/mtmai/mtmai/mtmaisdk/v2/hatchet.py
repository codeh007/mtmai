from typing import Callable, List, Optional, TypeVar

from mtmaisdk.context import Context
from mtmaisdk.contracts.workflows_pb2 import ConcurrencyLimitStrategy, StickyStrategy
from mtmaisdk.hatchet import Hatchet as HatchetV1
from mtmaisdk.hatchet import workflow
from mtmaisdk.labels import DesiredWorkerLabel
from mtmaisdk.rate_limit import RateLimit
from mtmaisdk.v2.callable import HatchetCallable
from mtmaisdk.v2.concurrency import ConcurrencyFunction
from mtmaisdk.worker.worker import register_on_worker

from ..worker import Worker

T = TypeVar("T")


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


class Hatchet(HatchetV1):
    dag = staticmethod(workflow)
    concurrency = staticmethod(concurrency)

    functions: List[HatchetCallable] = []

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
