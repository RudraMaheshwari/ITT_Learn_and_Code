from __future__ import annotations
from typing import Any
from ..core.base import StepExecutionError
from ..models.models import StepSpec, TraceEvent, Tracer, WorkflowState
from ..utils.event_builder import StepEventBuilder
from ..utils.factory import StepFactory

class StepExecutor:
    def __init__(self, tracer: Tracer | None = None) -> None:
        self._tracer = tracer
        self._event_builder = StepEventBuilder()
        self._factory = StepFactory()

    def execute_step(self, workflow_name: str, state: WorkflowState, step_spec: StepSpec) -> WorkflowState:
        result_state = state

        if not self._should_skip(workflow_name, state, step_spec):
            try:
                result_state = self._run_with_retry(workflow_name, state, step_spec)
            except StepExecutionError as exc:
                if not step_spec.on_failure:
                    raise exc
                result_state = self._execute_fallback(workflow_name, state, step_spec)

        return result_state

    def _should_skip(self, workflow_name: str, state: WorkflowState, spec: StepSpec) -> bool:
        skip = False
        if spec.condition is not None:
            condition_passed = self._factory.evaluate_condition(spec.condition, state)
            self._emit(self._event_builder.build_condition_evaluated_event(workflow_name, spec.condition, condition_passed))
            
            if not condition_passed:
                self._emit(self._event_builder.build_step_skipped_event(workflow_name, spec))
                skip = True
        return skip

    def _run_with_retry(self, workflow_name: str, state: WorkflowState, spec: StepSpec) -> WorkflowState:
        policy = spec.effective_retry()
        last_error: Exception | None = None
        result_state = None

        for attempt in range(1, policy.max_attempts + 1):
            self._emit(self._event_builder.build_step_start_event(workflow_name, spec, attempt))
            try:
                result_state = self._run_step_once(workflow_name, state, spec, attempt)
                break
            except Exception as step_error:
                last_error = step_error
                self._emit(self._event_builder.build_step_error_event(workflow_name, spec, attempt, step_error))

        if result_state is None:
            raise StepExecutionError(f"Step failed after retries: {spec.type}") from last_error

        return result_state

    def _run_step_once(self, workflow_name: str, state: WorkflowState, spec: StepSpec, attempt: int) -> WorkflowState:
        created_step = self._factory.create_step(spec.type, spec.effective_config())
        new_payload = created_step.run(state)
        new_state = state.replace_payload(new_payload)
        self._emit(self._event_builder.build_step_end_event(workflow_name, spec, attempt, new_payload))
        return new_state

    def _execute_fallback(self, workflow_name: str, state: WorkflowState, spec: StepSpec) -> WorkflowState:
        self._emit(self._event_builder.build_fallback_start_event(workflow_name, spec))
        return self.execute_step(workflow_name=workflow_name, state=state, step_spec=spec.on_failure)

    def _emit(self, event: TraceEvent) -> None:
        if self._tracer is None:
            return
        self._tracer.emit(event)

