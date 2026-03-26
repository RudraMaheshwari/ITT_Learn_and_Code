from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Callable, Generic, Mapping, TypeVar

T = TypeVar("T")

@dataclass(frozen=True, slots=True)
class PluginRegistration(Generic[T]):
    key: str
    factory: Callable[[Mapping[str, Any]], T]

class PluginRegistry(Generic[T]):
    def __init__(self, kind: str) -> None:
        self._kind = kind
        self._by_key: dict[str, Callable[[Mapping[str, Any]], T]] = {}

    def register(self, key: str) -> Callable[[type[T]], type[T]]:
        if not isinstance(key, str) or not key:
            raise ValueError("registry key must be a non-empty string")

        def decorator(plugin_class: type[T]) -> type[T]:
            if key in self._by_key:
                raise ValueError(f"Duplicate {self._kind} registration: {key}")

            def factory(plugin_config: Mapping[str, Any]) -> T:
                return plugin_class(plugin_config)

            self._by_key[key] = factory
            return plugin_class

        return decorator

    def create(self, key: str, config: Mapping[str, Any]) -> T:
        try:
            factory = self._by_key[key]
        except KeyError as registry_error:
            registered_keys = ", ".join(sorted(self._by_key.keys())) or "<none>"
            raise KeyError(f"Unknown {self._kind}: {key}. Known: {registered_keys}") from registry_error
        return factory(config)

step_registry: PluginRegistry[Any] = PluginRegistry(kind="step")
condition_registry: PluginRegistry[Any] = PluginRegistry(kind="condition")

