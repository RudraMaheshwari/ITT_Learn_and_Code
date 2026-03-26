# AI Prompt Orchestration Engine (Python)

Backend-style workflow engine to orchestrate **dynamic AI pipelines** with:

- Plug-and-play **steps** (Open–Closed Principle; add new step types without editing core)
- **Retries** (optional) per step
- **Fallback** step if a step fails
- **Conditional** steps (run only if a condition evaluates true)
- **Logging / tracing** for step timing, attempts, outputs, and failures

This is a Python refactor of the original C#-style "if/else stepType" design.

## Layout

- `src/core/registry.py` — step + condition registries (plugin mechanism)
- `src/core/orchestrator.py` — workflow runner (orchestration only)
- `src/core/tracing.py` — trace events + in-memory tracer
- `src/domain/workflow.py` — workflow + step specs (configuration objects)
- `src/domain/conditions.py` — condition interface + built-in conditions
- `src/steps/` — built-in step implementations (generate, summarize, translate, etc.)

## Run

```bash
python main.py
```

## Adding a new step type (no core edits)

1. Create a new file under `src/steps/`, implement `Step`.
2. Register it via `@step_registry.register("YOUR_TYPE")`.
3. Use `"type": "YOUR_TYPE"` in a `StepSpec`.

