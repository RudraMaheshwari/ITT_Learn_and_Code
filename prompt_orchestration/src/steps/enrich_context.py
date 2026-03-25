from __future__ import annotations
from typing import Any, Mapping
from ..config.constants import STEP_ENRICH_WITH_CONTEXT
from ..core.base import Step
from ..core.registry import step_registry
from ..domain.context import WorkflowState

@step_registry.register(STEP_ENRICH_WITH_CONTEXT)
class EnrichWithContextStep(Step):
    def __init__(self, config: Mapping[str, Any]) -> None:
        super().__init__(dict(config))
        raw_context_text = config.get("context_text", "")
        if not isinstance(raw_context_text, str):
            raise ValueError("ENRICH_WITH_CONTEXT requires 'context_text' (str)")
        self._context_text = raw_context_text.strip()

    def run(self, state: WorkflowState) -> Any:
        if not self._context_text:
            return state.current_payload
        return f"{self._context_text}\n\n{state.current_payload}"
