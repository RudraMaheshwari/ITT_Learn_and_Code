from __future__ import annotations
from typing import Any, Mapping
from ..config.constants import STEP_REFINE_TONE
from ..core.base import Step
from ..core.registry import step_registry
from ..domain.context import WorkflowState

@step_registry.register(STEP_REFINE_TONE)
class RefineToneStep(Step):
    def __init__(self, config: Mapping[str, Any]) -> None:
        super().__init__(dict(config))
        tone = config.get("tone", "neutral")
        if not isinstance(tone, str) or not tone.strip():
            raise ValueError("REFINE_TONE requires 'tone' (str)")
        self._tone = tone.strip()

    def run(self, state: WorkflowState) -> Any:
        return f"[Tone={self._tone}] {state.current_payload}"
