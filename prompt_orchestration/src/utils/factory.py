from __future__ import annotations
from typing import Mapping, Any
from ..core.base import Step
from ..core.registry import condition_registry, step_registry
from ..models.models import ConditionSpec, WorkflowState

class StepFactory:
    @staticmethod
    def create_step(spec_type: str, config: Mapping[str, Any]) -> Step:
        created_step = step_registry.create(spec_type, dict(config))
        if not isinstance(created_step, Step):
            raise TypeError(f"Registered step '{spec_type}' must inherit Step")
        return created_step

    @staticmethod
    def evaluate_condition(condition_spec: ConditionSpec, state: WorkflowState) -> bool:
        evaluated_condition = condition_registry.create(condition_spec.type, dict(condition_spec.effective_config()))
        return bool(evaluated_condition.evaluate(state))
