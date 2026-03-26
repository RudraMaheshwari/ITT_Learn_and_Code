from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Any, Mapping
from ..config.constants import COND_ALWAYS, COND_METADATA_EQUALS, COND_OUTPUT_CONTAINS
from ..core.registry import condition_registry
from ..models.models import WorkflowState

class Condition(ABC):
    @abstractmethod
    def evaluate(self, state: WorkflowState) -> bool:
        raise NotImplementedError

@condition_registry.register(COND_ALWAYS)
class AlwaysCondition(Condition):
    def __init__(self, _unused_config: Mapping[str, Any]) -> None:
        pass

    def evaluate(self, state: WorkflowState) -> bool:
        return True

@condition_registry.register(COND_OUTPUT_CONTAINS)
class OutputContainsCondition(Condition):
    def __init__(self, config: Mapping[str, Any]) -> None:
        required_substring = config.get("substring")
        if not isinstance(required_substring, str) or not required_substring:
            raise ValueError("OUTPUT_CONTAINS requires non-empty 'substring' (str)")
        self._required_substring = required_substring

    def evaluate(self, state: WorkflowState) -> bool:
        return self._required_substring in str(state.current_payload)

@condition_registry.register(COND_METADATA_EQUALS)
class MetadataEqualsCondition(Condition):
    def __init__(self, config: Mapping[str, Any]) -> None:
        metadata_key = config.get("key")
        if not isinstance(metadata_key, str) or not metadata_key:
            raise ValueError("METADATA_EQUALS requires non-empty 'key' (str)")
        self._metadata_key = metadata_key
        self._expected_value = config.get("value")

    def evaluate(self, state: WorkflowState) -> bool:
        return state.metadata.get(self._metadata_key) == self._expected_value

