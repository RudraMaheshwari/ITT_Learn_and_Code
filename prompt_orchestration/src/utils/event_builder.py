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
from ..core.tracing import utc_now
from ..models.models import ConditionSpec, StepSpec, TraceEvent

class StepEventBuilder:
    @staticmethod
    def build_step_skipped_event(workflow_name: str, step_spec: StepSpec) -> TraceEvent:
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

    @staticmethod
    def build_step_start_event(workflow_name: str, step_spec: StepSpec, attempt: int) -> TraceEvent:
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

    @staticmethod
    def build_step_end_event(workflow_name: str, step_spec: StepSpec, attempt: int, output_payload: Any) -> TraceEvent:
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

    @staticmethod
    def build_step_error_event(workflow_name: str, step_spec: StepSpec, attempt: int, step_error: Exception) -> TraceEvent:
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

    @staticmethod
    def build_fallback_start_event(workflow_name: str, step_spec: StepSpec) -> TraceEvent:
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

    @staticmethod
    def build_condition_evaluated_event(workflow_name: str, condition: ConditionSpec, condition_passed: bool) -> TraceEvent:
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
