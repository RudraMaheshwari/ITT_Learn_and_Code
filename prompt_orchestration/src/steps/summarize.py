from __future__ import annotations
from typing import Any, Mapping
from ..config.constants import DEFAULT_SUMMARY_MAX_LEN, MIN_SUMMARY_MAX_LEN, STEP_SUMMARIZE, SUMMARY_PREFIX
from ..core.base import Step
from ..core.registry import step_registry
from ..domain.context import WorkflowState

@step_registry.register(STEP_SUMMARIZE)
class SummarizeStep(Step):
    def __init__(self, config: Mapping[str, Any]) -> None:
        super().__init__(dict(config))
        maximum_summary_length = config.get("max_len", DEFAULT_SUMMARY_MAX_LEN)
        if not isinstance(maximum_summary_length, int) or maximum_summary_length < MIN_SUMMARY_MAX_LEN:
            raise ValueError(f"SUMMARIZE requires 'max_len' as int >= {MIN_SUMMARY_MAX_LEN}")
        self._maximum_summary_length = maximum_summary_length

    def run(self, state: WorkflowState) -> Any:
        full_text = str(state.current_payload)
        if len(full_text) <= self._maximum_summary_length:
            return f"{SUMMARY_PREFIX}{full_text}"
        return f"{SUMMARY_PREFIX}{full_text[:self._maximum_summary_length].rstrip()}..."
