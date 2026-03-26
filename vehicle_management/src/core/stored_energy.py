from __future__ import annotations
from ..utils.validation import percent_after_increase, validated_stored_energy_percent

class StoredEnergyPercent:
    def __init__(self, initial_percent: float) -> None:
        self._percent = validated_stored_energy_percent(initial_percent)

    @property
    def percent(self) -> float:
        return self._percent

    def add_percent(self, delta: float) -> float:
        self._percent = percent_after_increase(self._percent, delta)
        return self._percent

