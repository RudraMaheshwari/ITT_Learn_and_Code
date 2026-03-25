from __future__ import annotations
from typing import Any, Mapping
from ..config.constants import ALLOWED_POST_PROCESS_MODES, STEP_POST_PROCESS
from ..core.base import Step
from ..core.registry import step_registry
from ..domain.context import WorkflowState

@step_registry.register(STEP_POST_PROCESS)
class PostProcessStep(Step):
    def __init__(self, config: Mapping[str, Any]) -> None:
        super().__init__(dict(config))
        mode = config.get("mode", "strip")
        if mode not in ALLOWED_POST_PROCESS_MODES:
            raise ValueError("POST_PROCESS mode must be one of: strip, upper, lower")
        self._mode = mode

    def run(self, state: WorkflowState) -> Any:
        raw_text = str(state.current_payload)
        return self._apply_mode(raw_text)

    def _apply_mode(self, raw_text: str) -> str:
        if self._mode == "strip":
            return raw_text.strip()
        if self._mode == "upper":
            return raw_text.upper()
        return raw_text.lower()
