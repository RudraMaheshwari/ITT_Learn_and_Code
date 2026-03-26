from __future__ import annotations
from abc import ABC, abstractmethod
from ..monetization_context import MonetizationContext

class EarningStrategy(ABC):
    @abstractmethod
    def label(self) -> str:
        raise NotImplementedError

    @abstractmethod
    def calculate(self, context: MonetizationContext) -> float:
        raise NotImplementedError

