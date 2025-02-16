from typing import TypedDict


class DesiredWorkerLabel(TypedDict):
    value: str | int
    required: bool | None = None
    weight: int | None = None
    comparator: int | None = (
        None  # _ClassVar[WorkerLabelComparator] TODO figure out type
    )


from dataclasses import dataclass


@dataclass
class RateLimit:
    key: str
    units: int


class RateLimitDuration:
    SECOND = "SECOND"
    MINUTE = "MINUTE"
    HOUR = "HOUR"
