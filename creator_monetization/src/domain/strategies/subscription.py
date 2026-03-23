from __future__ import annotations
from ...config.constants import (
    SUBSCRIPTION_ENGAGEMENT_WEIGHT,
    SUBSCRIPTION_REVENUE_PER_SUBSCRIBER,
)
from ...utils.factors import regional_multiplier, seasonal_multiplier
from ..monetization_context import MonetizationContext
from .earning_strategy import EarningStrategy

class SubscriptionStrategy(EarningStrategy):
    def label(self) -> str:
        return "Subscriptions"

    def calculate(self, context: MonetizationContext) -> float:
        base = context.subscribers * SUBSCRIPTION_REVENUE_PER_SUBSCRIBER
        engagement_factor = 1.0 + SUBSCRIPTION_ENGAGEMENT_WEIGHT * context.engagement_rate
        return (
            base
            * engagement_factor
            * regional_multiplier(context.region)
            * seasonal_multiplier(context.season)
        )
