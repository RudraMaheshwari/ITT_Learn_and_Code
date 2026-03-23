from __future__ import annotations
from ...config.constants import AD_ENGAGEMENT_BASE_MULTIPLIER, AD_ENGAGEMENT_WEIGHT, AD_REVENUE_PER_VIEW
from ...utils.factors import regional_multiplier, seasonal_multiplier
from ..monetization_context import MonetizationContext
from .earning_strategy import EarningStrategy

class AdRevenueStrategy(EarningStrategy):
    def label(self) -> str:
        return "Ad revenue"

    def calculate(self, context: MonetizationContext) -> float:
        base = context.views * AD_REVENUE_PER_VIEW
        engagement_factor = (
            AD_ENGAGEMENT_BASE_MULTIPLIER
            + AD_ENGAGEMENT_WEIGHT * context.engagement_rate
        )
        return (
            base
            * engagement_factor
            * regional_multiplier(context.region)
            * seasonal_multiplier(context.season)
        )
