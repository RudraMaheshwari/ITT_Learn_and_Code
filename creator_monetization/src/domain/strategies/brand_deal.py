from __future__ import annotations
from ...utils.factors import regional_multiplier
from ...utils.validation import require_non_negative_amount
from ..monetization_context import MonetizationContext
from .earning_strategy import EarningStrategy

class BrandDealStrategy(EarningStrategy):
    def __init__(self, contracted_amount: float) -> None:
        require_non_negative_amount("contracted_amount", contracted_amount)
        self._contracted_amount = contracted_amount

    def label(self) -> str:
        return "Brand deal"

    def calculate(self, context: MonetizationContext) -> float:
        return self._contracted_amount * regional_multiplier(context.region)

