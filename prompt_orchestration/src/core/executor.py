from __future__ import annotations
from typing import Any
from ..config.constants import (
    MSG_CONDITION_FALSE,
    MSG_EXECUTING_FALLBACK,
    TRACE_CONDITION_EVALUATED,
    TRACE_OUTPUT_PREVIEW_MAX_CHARS,
    TRACE_STEP_END,
    TRACE_STEP_ERROR,
    TRACE_STEP_FALLBACK_START,
    TRACE_STEP_SKIPPED,
    TRACE_STEP_START,
)
from ..core.base import Step, StepExecutionError
from ..core.registry import condition_registry, step_registry
from ..core.tracing import utc_now
from ..models.models import ConditionSpec, StepSpec, TraceEvent, Tracer, WorkflowState

class StepExecutor:
    def __init__(self, tracer: Tracer | None = None) -> None:
        self._tracer = tracer

    def execute_step(self, workflow_name: str, state: WorkflowState, step_spec: StepSpec) -> WorkflowState:
        if step_spec.condition is not None:
            should_run = self._evaluate_condition(workflow_name=workflow_name, state=state, condition=step_spec.condition)
            if not should_run:
                self._emit(self._build_step_skipped_event(workflow_name, step_spec))
                return state

        policy = step_spec.effective_retry()
        last_error: Exception | None = None

        for attempt in range(1, policy.max_attempts + 1):
            self._emit(self._build_step_start_event(workflow_name, step_spec, attempt))

            try:
                created_step = self._create_step(step_spec)
                new_payload = created_step.run(state)
                new_state = state.replace_payload(new_payload)
                self._emit(self._build_step_end_event(workflow_name, step_spec, attempt, new_payload))
                return new_state
            except Exception as step_error:
                last_error = step_error
                self._emit(self._build_step_error_event(workflow_name, step_spec, attempt, step_error))

        if step_spec.on_failure is not None:
            self._emit(self._build_fallback_start_event(workflow_name, step_spec))
            return self.execute_step(workflow_name=workflow_name, state=state, step_spec=step_spec.on_failure)

        raise StepExecutionError(f"Step failed after retries: {step_spec.type}") from last_error

    def _create_step(self, spec: StepSpec) -> Step:
        created_step = step_registry.create(spec.type, dict(spec.effective_config()))
        if not isinstance(created_step, Step):
            raise TypeError(f"Registered step '{spec.type}' must inherit Step")
        return created_step

    def _evaluate_condition(self, workflow_name: str, state: WorkflowState, condition: ConditionSpec) -> bool:
        evaluated_condition = condition_registry.create(condition.type, dict(condition.effective_config()))
        condition_passed = bool(evaluated_condition.evaluate(state))
        self._emit(self._build_condition_evaluated_event(workflow_name, condition, condition_passed))
        return condition_passed

    def _emit(self, event: TraceEvent) -> None:
        if self._tracer is None:
            return
        self._tracer.emit(event)

    def _build_step_skipped_event(self, workflow_name: str, step_spec: StepSpec) -> TraceEvent:
        return TraceEvent(
            kind=TRACE_STEP_SKIPPED,
            workflow_name=workflow_name,
            step_type=step_spec.type,
            attempt=None,
            ok=True,
            message=MSG_CONDITION_FALSE,
            timestamp_utc=utc_now(),
            details={"condition_type": step_spec.condition.type if step_spec.condition else None},
        )

    def _build_step_start_event(self, workflow_name: str, step_spec: StepSpec, attempt: int) -> TraceEvent:
        return TraceEvent(
            kind=TRACE_STEP_START,
            workflow_name=workflow_name,
            step_type=step_spec.type,
            attempt=attempt,
            ok=None,
            message=None,
            timestamp_utc=utc_now(),
            details={"config": dict(step_spec.effective_config())},
        )

    def _build_step_end_event(self, workflow_name: str, step_spec: StepSpec, attempt: int, output_payload: Any) -> TraceEvent:
        return TraceEvent(
            kind=TRACE_STEP_END,
            workflow_name=workflow_name,
            step_type=step_spec.type,
            attempt=attempt,
            ok=True,
            message=None,
            timestamp_utc=utc_now(),
            details={"output_preview": str(output_payload)[:TRACE_OUTPUT_PREVIEW_MAX_CHARS]},
        )

    def _build_step_error_event(self, workflow_name: str, step_spec: StepSpec, attempt: int, step_error: Exception) -> TraceEvent:
        return TraceEvent(
            kind=TRACE_STEP_ERROR,
            workflow_name=workflow_name,
            step_type=step_spec.type,
            attempt=attempt,
            ok=False,
            message=str(step_error),
            timestamp_utc=utc_now(),
            details={"error_type": type(step_error).__name__},
        )

    def _build_fallback_start_event(self, workflow_name: str, step_spec: StepSpec) -> TraceEvent:
        return TraceEvent(
            kind=TRACE_STEP_FALLBACK_START,
            workflow_name=workflow_name,
            step_type=step_spec.type,
            attempt=None,
            ok=None,
            message=MSG_EXECUTING_FALLBACK,
            timestamp_utc=utc_now(),
            details={"fallback_type": step_spec.on_failure.type if step_spec.on_failure else None},
        )

    def _build_condition_evaluated_event(self, workflow_name: str, condition: ConditionSpec, condition_passed: bool) -> TraceEvent:
        return TraceEvent(
            kind=TRACE_CONDITION_EVALUATED,
            workflow_name=workflow_name,
            step_type=None,
            attempt=None,
            ok=condition_passed,
            message=None,
            timestamp_utc=utc_now(),
            details={"condition_type": condition.type},
        )
