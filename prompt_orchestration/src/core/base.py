from __future__ import annotations
from typing import Any
from ..models.models import WorkflowState

class StepExecutionError(RuntimeError):
    ...

class Step:
    def __init__(self, config: dict[str, Any]) -> None:
        self._config = dict(config)

    def run(self, state: WorkflowState) -> Any:
        raise NotImplementedError
