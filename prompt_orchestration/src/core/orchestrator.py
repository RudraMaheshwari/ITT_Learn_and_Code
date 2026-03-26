from __future__ import annotations
from typing import Any
from ..config.constants import (
    TRACE_WORKFLOW_END,
    TRACE_WORKFLOW_START,
)
from ..core.executor import build_default_executor
from ..core.tracing import utc_now
from ..models.models import (
    TraceEvent,
    Tracer,
    WorkflowRunResult,
    WorkflowSpec,
    WorkflowState,
)

class WorkflowOrchestrator:
    def __init__(self, tracer: Tracer | None = None) -> None:
        self._tracer = tracer
        self._executor = build_default_executor(tracer=tracer)

    def run(self, workflow: WorkflowSpec, initial_input: Any, metadata: dict[str, Any] | None = None) -> WorkflowRunResult:
        state = WorkflowState(current_payload=initial_input, metadata=metadata or {})

        self._emit(self._build_workflow_start_event(workflow.name, initial_input))

        for step_spec in workflow.steps:
            state = self._executor.execute_step(workflow_name=workflow.name, state=state, step_spec=step_spec)

        self._emit(self._build_workflow_end_event(workflow.name, state.current_payload))

        return WorkflowRunResult(output=state.current_payload, state=state)

    def _emit(self, event: TraceEvent) -> None:
        if self._tracer is None:
            return
        self._tracer.emit(event)

    def _build_workflow_start_event(self, workflow_name: str, initial_input: Any) -> TraceEvent:
        return TraceEvent(
            kind=TRACE_WORKFLOW_START,
            workflow_name=workflow_name,
            step_type=None,
            attempt=None,
            ok=None,
            message=None,
            timestamp_utc=utc_now(),
            details={"initial_input": str(initial_input)},
        )

    def _build_workflow_end_event(self, workflow_name: str, final_output: Any) -> TraceEvent:
        return TraceEvent(
            kind=TRACE_WORKFLOW_END,
            workflow_name=workflow_name,
            step_type=None,
            attempt=None,
            ok=True,
            message=None,
            timestamp_utc=utc_now(),
            details={"final_output": str(final_output)},
        )

