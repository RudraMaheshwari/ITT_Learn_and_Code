from __future__ import annotations
from .monetization_context import MonetizationContext
from .strategies.earning_strategy import EarningStrategy

class Creator:
    def __init__(self, name: str) -> None:
        self._name = name.strip()
        self._earning_sources: list[EarningStrategy] = []

    @property
    def name(self) -> str:
        return self._name

    def attach_earning_source(self, source: EarningStrategy) -> None:
        self._earning_sources.append(source)

    def total_earnings(self, context: MonetizationContext) -> float:
        return sum(source.calculate(context) for source in self._earning_sources)

    def earnings_breakdown(self, context: MonetizationContext) -> tuple[tuple[str, float], ...]:
        rows: list[tuple[str, float]] = []
        for source in self._earning_sources:
            amount = source.calculate(context)
            rows.append((source.label(), amount))
        return tuple(rows)
