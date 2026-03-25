from __future__ import annotations
from typing import Any, Mapping
from ..config.constants import (
    ERR_SIMULATED_TRANSLATION_FAILURE,
    STEP_TRANSLATE,
    TRANSLATED_PREFIX_FMT,
)
from ..core.base import Step
from ..core.registry import step_registry
from ..domain.context import WorkflowState

@step_registry.register(STEP_TRANSLATE)
class TranslateStep(Step):
    def __init__(self, config: Mapping[str, Any]) -> None:
        super().__init__(dict(config))
        raw_target_language = config.get("target_language")
        if not isinstance(raw_target_language, str) or not raw_target_language.strip():
            raise ValueError("TRANSLATE requires 'target_language' (str)")
        self._target_language = raw_target_language.strip()
        self._should_simulate_failure = bool(config.get("fail", False))

    def run(self, state: WorkflowState) -> Any:
        if self._should_simulate_failure:
            raise RuntimeError(ERR_SIMULATED_TRANSLATION_FAILURE)
        return f"{TRANSLATED_PREFIX_FMT.format(lang=self._target_language)}{state.current_payload}"
