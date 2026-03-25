from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Callable, Generic, Mapping, Protocol, Sequence, TypeVar

@dataclass(frozen=True, slots=True)
class WorkflowState:

    current_payload: Any
    metadata: dict[str, Any] = field(default_factory=dict)

    def replace_payload(self, new_payload: Any) -> "WorkflowState":
        return WorkflowState(current_payload=new_payload, metadata=dict(self.metadata))

    def merge_metadata(self, **updates: Any) -> "WorkflowState":
        updated_metadata = dict(self.metadata)
        updated_metadata.update(updates)
        return WorkflowState(current_payload=self.current_payload, metadata=updated_metadata)

@dataclass(frozen=True, slots=True)
class RetryPolicy:
    max_attempts: int = 1

    def __post_init__(self) -> None:
        if self.max_attempts < 1:
            raise ValueError("RetryPolicy.max_attempts must be >= 1")

@dataclass(frozen=True, slots=True)
class ConditionSpec:
    type: str
    config: Mapping[str, Any] | None = None

    def effective_config(self) -> Mapping[str, Any]:
        return self.config or {}

@dataclass(frozen=True, slots=True)
class StepSpec:
    type: str
    config: Mapping[str, Any] | None = None
    retry: RetryPolicy | None = None
    condition: ConditionSpec | None = None
    on_failure: "StepSpec | None" = None

    def effective_config(self) -> Mapping[str, Any]:
        return self.config or {}

    def effective_retry(self) -> RetryPolicy:
        return self.retry or RetryPolicy()

@dataclass(frozen=True, slots=True)
class WorkflowSpec:
    name: str
    steps: Sequence[StepSpec]

@dataclass(frozen=True, slots=True)
class TraceEvent:
    kind: str
    workflow_name: str
    step_type: str | None
    attempt: int | None
    ok: bool | None
    message: str | None
    timestamp_utc: datetime
    details: dict[str, Any]

class Tracer(Protocol):
    def emit(self, event: TraceEvent) -> None: ...

T = TypeVar("T")

@dataclass(frozen=True, slots=True)
class WorkflowRunResult:
    output: Any
    state: WorkflowState
