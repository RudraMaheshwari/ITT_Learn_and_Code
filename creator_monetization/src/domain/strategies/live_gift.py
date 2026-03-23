from __future__ import annotations
from ...config.constants import LIVE_GIFT_AVG_PAYOUT, LIVE_GIFT_ENGAGEMENT_WEIGHT
from ...utils.factors import regional_multiplier, seasonal_multiplier
from ..monetization_context import MonetizationContext
from .earning_strategy import EarningStrategy

class LiveGiftStrategy(EarningStrategy):
    def label(self) -> str:
        return "Live gifts"

    def calculate(self, context: MonetizationContext) -> float:
        base = context.live_gift_units * LIVE_GIFT_AVG_PAYOUT
        engagement_factor = 1.0 + LIVE_GIFT_ENGAGEMENT_WEIGHT * context.engagement_rate
        return (
            base
            * engagement_factor
            * regional_multiplier(context.region)
            * seasonal_multiplier(context.season)
        )
