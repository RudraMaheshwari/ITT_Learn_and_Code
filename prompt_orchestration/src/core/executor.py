from __future__ import annotations
from typing import Protocol
from ..core.base import StepExecutionError
from ..models.models import StepSpec, TraceEvent, Tracer, WorkflowState
from ..utils.event_builder import StepEventBuilder
from ..utils.factory import StepFactory

class StepExecutor(Protocol):
    def execute_step(self, workflow_name: str, state: WorkflowState, step_spec: StepSpec) -> WorkflowState:
        ...

class AttemptExecutor(Protocol):
    def execute_attempt(self, workflow_name: str, state: WorkflowState, step_spec: StepSpec, attempt: int) -> WorkflowState:
        ...

class CoreStepExecutor(AttemptExecutor):
    def __init__(self, factory: StepFactory) -> None:
        self._factory = factory

    def execute_attempt(self, workflow_name: str, state: WorkflowState, step_spec: StepSpec, attempt: int) -> WorkflowState:
        created_step = self._factory.create_step(step_spec.type, step_spec.effective_config())
        new_payload = created_step.run(state)
        return state.replace_payload(new_payload)

class TracingAttemptExecutor(AttemptExecutor):
    def __init__(self, inner: AttemptExecutor, tracer: Tracer | None, event_builder: StepEventBuilder) -> None:
        self._inner = inner
        self._tracer = tracer
        self._event_builder = event_builder

    def execute_attempt(self, workflow_name: str, state: WorkflowState, step_spec: StepSpec, attempt: int) -> WorkflowState:
        self._emit(self._event_builder.build_step_start_event(workflow_name, step_spec, attempt))
        try:
            result_state = self._inner.execute_attempt(workflow_name, state, step_spec, attempt)
            self._emit(self._event_builder.build_step_end_event(workflow_name, step_spec, attempt, result_state.current_payload))
            return result_state
        except Exception as step_error:
            self._emit(self._event_builder.build_step_error_event(workflow_name, step_spec, attempt, step_error))
            raise

    def _emit(self, event: TraceEvent) -> None:
        if self._tracer is not None:
            self._tracer.emit(event)

class RetryStepExecutor(StepExecutor):
    def __init__(self, inner: AttemptExecutor) -> None:
        self._inner = inner

    def execute_step(self, workflow_name: str, state: WorkflowState, step_spec: StepSpec) -> WorkflowState:
        policy = step_spec.effective_retry()
        last_error: Exception | None = None

        for attempt in range(1, policy.max_attempts + 1):
            try:
                return self._inner.execute_attempt(workflow_name, state, step_spec, attempt)
            except Exception as e:
                last_error = e

        raise StepExecutionError(f"Step failed after retries: {step_spec.type}") from last_error

class FallbackStepExecutor(StepExecutor):
    def __init__(self, inner: StepExecutor, tracer: Tracer | None, event_builder: StepEventBuilder) -> None:
        self._inner = inner
        self._tracer = tracer
        self._event_builder = event_builder
        self._top_level: StepExecutor | None = None

    def set_top_level(self, top_level: StepExecutor) -> None:
        self._top_level = top_level

    def execute_step(self, workflow_name: str, state: WorkflowState, step_spec: StepSpec) -> WorkflowState:
        try:
            return self._inner.execute_step(workflow_name, state, step_spec)
        except StepExecutionError as exc:
            if not step_spec.on_failure:
                raise exc
            
            self._emit(self._event_builder.build_fallback_start_event(workflow_name, step_spec))
            if self._top_level is None:
                raise RuntimeError("Top-level executor not set for fallback execution.")
            return self._top_level.execute_step(workflow_name, state, step_spec.on_failure)

    def _emit(self, event: TraceEvent) -> None:
        if self._tracer is not None:
            self._tracer.emit(event)

class ConditionStepExecutor(StepExecutor):
    def __init__(self, inner: StepExecutor, factory: StepFactory, tracer: Tracer | None, event_builder: StepEventBuilder) -> None:
        self._inner = inner
        self._factory = factory
        self._tracer = tracer
        self._event_builder = event_builder

    def execute_step(self, workflow_name: str, state: WorkflowState, step_spec: StepSpec) -> WorkflowState:
        if step_spec.condition is not None:
            condition_passed = self._factory.evaluate_condition(step_spec.condition, state)
            self._emit(self._event_builder.build_condition_evaluated_event(workflow_name, step_spec.condition, condition_passed))
            
            if not condition_passed:
                self._emit(self._event_builder.build_step_skipped_event(workflow_name, step_spec))
                return state
        
        return self._inner.execute_step(workflow_name, state, step_spec)

    def _emit(self, event: TraceEvent) -> None:
        if self._tracer is not None:
            self._tracer.emit(event)

def build_default_executor(tracer: Tracer | None = None) -> StepExecutor:
    factory = StepFactory()
    event_builder = StepEventBuilder()
    
    core = CoreStepExecutor(factory)
    tracing = TracingAttemptExecutor(core, tracer, event_builder)
    retry = RetryStepExecutor(tracing)
    fallback = FallbackStepExecutor(retry, tracer, event_builder)
    condition = ConditionStepExecutor(fallback, factory, tracer, event_builder)
    
    fallback.set_top_level(condition)
    
    return condition

