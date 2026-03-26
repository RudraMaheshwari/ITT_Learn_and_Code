from __future__ import annotations
from typing import Any, Mapping
from ..config.constants import STEP_NOOP
from ..core.base import Step
from ..core.registry import step_registry
from ..domain.context import WorkflowState

@step_registry.register(STEP_NOOP)
class NoopStep(Step):
    def __init__(self, config: Mapping[str, Any]) -> None:
        super().__init__(dict(config))
        self._reason = str(config.get("reason") or "").strip()

    def run(self, state: WorkflowState) -> Any:
        return state.current_payload

