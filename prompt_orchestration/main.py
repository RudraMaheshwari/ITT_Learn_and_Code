from __future__ import annotations
from prompt_orchestration.src.core.orchestrator import WorkflowOrchestrator
from prompt_orchestration.src.core.tracing import InMemoryTracer
from prompt_orchestration.src.config.constants import (
    COND_OUTPUT_CONTAINS,
    DEFAULT_GENERATE_PREFIX,
    DEMO_INITIAL_INPUT,
    STEP_GENERATE,
    STEP_NOOP,
    STEP_REFINE_TONE,
    STEP_SUMMARIZE,
    STEP_TRANSLATE,
)
from prompt_orchestration.src.models.models import ConditionSpec, RetryPolicy, StepSpec, WorkflowSpec
from prompt_orchestration.src import builtins

def main() -> None:
    tracer = InMemoryTracer()
    orchestrator = WorkflowOrchestrator(tracer=tracer)

    workflow = WorkflowSpec(
        name="Product description pipeline",
        steps=[
            StepSpec(type=STEP_GENERATE, config={"prefix": DEFAULT_GENERATE_PREFIX}),
            StepSpec(type=STEP_REFINE_TONE, config={"tone": "friendly"}),
            StepSpec(
                type=STEP_SUMMARIZE,
                retry=RetryPolicy(max_attempts=2),
            ),
            StepSpec(
                type=STEP_TRANSLATE,
                config={"target_language": "es"},
                condition=ConditionSpec(type=COND_OUTPUT_CONTAINS, config={"substring": "Generated"}),
                on_failure=StepSpec(type=STEP_NOOP, config={"reason": "translate failed; keeping original"}),
            ),
        ],
    )

    workflow_result = orchestrator.run(workflow=workflow, initial_input=DEMO_INITIAL_INPUT)

    print("FINAL OUTPUT")
    print(workflow_result.output)
    print()

    print("TRACE (most recent run)")
    for trace_event in tracer.events:
        print(f"- {trace_event.kind} step={trace_event.step_type} attempt={trace_event.attempt} ok={trace_event.ok} msg={trace_event.message}")

if __name__ == "__main__":
    main()
