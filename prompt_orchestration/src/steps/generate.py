from __future__ import annotations
from typing import Any, Mapping
from ..config.constants import DEFAULT_GENERATE_PREFIX, STEP_GENERATE
from ..core.base import Step
from ..core.registry import step_registry
from ..domain.context import WorkflowState

@step_registry.register(STEP_GENERATE)
class GenerateStep(Step):
    def __init__(self, config: Mapping[str, Any]) -> None:
        super().__init__(dict(config))
        self._prefix = str(config.get("prefix") or DEFAULT_GENERATE_PREFIX)

    def run(self, state: WorkflowState) -> Any:
        return f"{self._prefix}{state.current_payload}"

