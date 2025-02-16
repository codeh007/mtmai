import asyncio
from typing import Callable, Dict, Generic, List, Optional, TypedDict, TypeVar, Union

from loguru import logger

from mtmai.context.context import Context
from mtmai.contracts.workflows_pb2 import (
    ConcurrencyLimitStrategy,
    CreateStepRateLimit,
    CreateWorkflowJobOpts,
    CreateWorkflowStepOpts,
    CreateWorkflowVersionOpts,
    DesiredWorkerLabels,
    StickyStrategy,
    WorkflowConcurrencyOpts,
    WorkflowKind,
)
from mtmai.models._types import DesiredWorkerLabel, RateLimit
from mtmai.workflow_run import RunRef

T = TypeVar("T")


class ConcurrencyFunction:
    def __init__(
        self,
        func: Callable[[Context], str],
        name: str = "concurrency",
        max_runs: int = 1,
        limit_strategy: ConcurrencyLimitStrategy = ConcurrencyLimitStrategy.GROUP_ROUND_ROBIN,
    ):
        self.func = func
        self.name = name
        self.max_runs = max_runs
        self.limit_strategy = limit_strategy
        self.namespace = "default"

    def set_namespace(self, namespace: str):
        self.namespace = namespace

    def get_action_name(self) -> str:
        return self.namespace + ":" + self.name

    def __call__(self, *args, **kwargs):
        return self.func(*args, **kwargs)

    def __str__(self):
        return f"{self.name}({self.max_runs})"

    def __repr__(self):
        return f"{self.name}({self.max_runs})"


class HatchetCallable(Generic[T]):
    def __init__(
        self,
        func: Callable[[Context], T],
        durable: bool = False,
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
        concurrency: ConcurrencyFunction | None = None,
        on_failure: Optional["HatchetCallable"] = None,
        desired_worker_labels: dict[str:DesiredWorkerLabel] = {},
        default_priority: int | None = None,
    ):
        self.func = func

        on_events = on_events or []
        on_crons = on_crons or []

        limits = None
        if rate_limits:
            limits = [
                CreateStepRateLimit(key=rate_limit.key, units=rate_limit.units)
                for rate_limit in rate_limits or []
            ]

        self.function_desired_worker_labels = {}

        for key, d in desired_worker_labels.items():
            value = d["value"] if "value" in d else None
            self.function_desired_worker_labels[key] = DesiredWorkerLabels(
                strValue=str(value) if not isinstance(value, int) else None,
                intValue=value if isinstance(value, int) else None,
                required=d["required"] if "required" in d else None,
                weight=d["weight"] if "weight" in d else None,
                comparator=d["comparator"] if "comparator" in d else None,
            )
        self.sticky = sticky
        self.default_priority = default_priority
        self.durable = durable
        self.function_name = name.lower() or str(func.__name__).lower()
        self.function_version = version
        self.function_on_events = on_events
        self.function_on_crons = on_crons
        self.function_timeout = timeout
        self.function_schedule_timeout = schedule_timeout
        self.function_retries = retries
        self.function_rate_limits = limits
        self.function_concurrency = concurrency
        self.function_on_failure = on_failure
        self.function_namespace = "default"
        self.function_auto_register = auto_register

        self.is_coroutine = False

        if asyncio.iscoroutinefunction(func):
            self.is_coroutine = True

    def __call__(self, context: Context) -> T:
        return self.func(context)

    def with_namespace(self, namespace: str):
        if namespace is not None and namespace != "":
            self.function_namespace = namespace
            self.function_name = namespace + self.function_name

    def to_workflow_opts(self) -> CreateWorkflowVersionOpts:
        kind: WorkflowKind = WorkflowKind.FUNCTION

        if self.durable:
            kind = WorkflowKind.DURABLE

        on_failure_job: CreateWorkflowJobOpts | None = None

        if self.function_on_failure is not None:
            on_failure_job = CreateWorkflowJobOpts(
                name=self.function_name + "-on-failure",
                steps=[
                    self.function_on_failure.to_step(),
                ],
            )

        concurrency: WorkflowConcurrencyOpts | None = None

        if self.function_concurrency is not None:
            self.function_concurrency.set_namespace(self.function_namespace)
            concurrency = WorkflowConcurrencyOpts(
                action=self.function_concurrency.get_action_name(),
                max_runs=self.function_concurrency.max_runs,
                limit_strategy=self.function_concurrency.limit_strategy,
            )

        validated_priority = (
            max(1, min(3, self.default_priority)) if self.default_priority else None
        )
        if validated_priority != self.default_priority:
            logger.warning(
                "Warning: Default Priority Must be between 1 and 3 -- inclusively. Adjusted to be within the range."
            )

        return CreateWorkflowVersionOpts(
            name=self.function_name,
            kind=kind,
            version=self.function_version,
            event_triggers=self.function_on_events,
            cron_triggers=self.function_on_crons,
            schedule_timeout=self.function_schedule_timeout,
            sticky=self.sticky,
            on_failure_job=on_failure_job,
            concurrency=concurrency,
            jobs=[
                CreateWorkflowJobOpts(
                    name=self.function_name,
                    steps=[
                        self.to_step(),
                    ],
                )
            ],
            default_priority=validated_priority,
        )

    def to_step(self) -> CreateWorkflowStepOpts:
        return CreateWorkflowStepOpts(
            readable_id=self.function_name,
            action=self.get_action_name(),
            timeout=self.function_timeout,
            inputs="{}",
            parents=[],
            retries=self.function_retries,
            rate_limits=self.function_rate_limits,
            worker_labels=self.function_desired_worker_labels,
        )

    def get_action_name(self) -> str:
        return self.function_namespace + ":" + self.function_name


class TriggerOptions(TypedDict):
    additional_metadata: Dict[str, str] | None = None
    sticky: bool | None = None


class DurableContext(Context):
    def run(
        self,
        function: Union[str, HatchetCallable[T]],
        input: dict = {},
        key: str = None,
        options: TriggerOptions = None,
    ) -> "RunRef[T]":
        worker_id = self.worker.id()

        workflow_name = function

        if not isinstance(function, str):
            workflow_name = function.function_name

        # if (
        #     options is not None
        #     and "sticky" in options
        #     and options["sticky"] == True
        #     and not self.worker.has_workflow(workflow_name)
        # ):
        #     raise Exception(
        #         f"cannot run with sticky: workflow {workflow_name} is not registered on the worker"
        #     )

        trigger_options = self._prepare_workflow_options(key, options, worker_id)

        return self.admin_client.run(function, input, trigger_options)
