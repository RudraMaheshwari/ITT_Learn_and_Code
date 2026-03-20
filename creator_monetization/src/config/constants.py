from __future__ import annotations
from typing import Final

AD_REVENUE_PER_VIEW: Final[float] = 0.05
AD_ENGAGEMENT_WEIGHT: Final[float] = 0.25

SUBSCRIPTION_REVENUE_PER_SUBSCRIBER: Final[float] = 2.0
SUBSCRIPTION_ENGAGEMENT_WEIGHT: Final[float] = 0.1

LIVE_GIFT_AVG_PAYOUT: Final[float] = 0.75
LIVE_GIFT_ENGAGEMENT_WEIGHT: Final[float] = 0.15

REGION_MULTIPLIERS: Final[dict[str, float]] = {
    "US": 1.0,
    "EU": 1.08,
    "IN": 0.92,
    "LATAM": 0.88,
    "DEFAULT": 1.0,
}

SEASON_MULTIPLIERS: Final[dict[str, float]] = {
    "WINTER": 1.0,
    "SPRING": 1.05,
    "SUMMER": 1.12,
    "FALL": 1.03,
    "DEFAULT": 1.0,
}

DEFAULT_REGION_KEY: Final[str] = "DEFAULT"
DEFAULT_SEASON_KEY: Final[str] = "DEFAULT"

DEMO_TITLE: Final[str] = "=== Creator Monetization Platform (refactored) ===\n"
DEMO_CREATOR_LABEL: Final[str] = "Creator: {name}"
DEMO_SOURCES_HEADER: Final[str] = "\nEarnings by source (same period):"
DEMO_SOURCE_LINE: Final[str] = "  • {label}: ${amount:,.2f}"
DEMO_TOTAL_LINE: Final[str] = "\nTotal estimated earnings: ${total:,.2f}"
DEMO_SCENARIO_NOTE: Final[str] = (
    "\n(Context: engagement + region + season multipliers apply where configured.)"
)

DEMO_CREATOR_DISPLAY_NAME: Final[str] = "Alex Rivers"
DEMO_BRAND_DEAL_AMOUNT: Final[float] = 5_000.0
DEMO_VIEWS: Final[int] = 120_000
DEMO_SUBSCRIBERS: Final[int] = 4_200
DEMO_ENGAGEMENT_RATE: Final[float] = 0.18
DEMO_LIVE_GIFT_UNITS: Final[int] = 3_400
DEMO_REGION_PRIMARY: Final[str] = "EU"
DEMO_SEASON_PRIMARY: Final[str] = "SUMMER"
DEMO_REGION_ALT: Final[str] = "IN"
DEMO_SEASON_ALT: Final[str] = "WINTER"
DEMO_SECOND_SCENARIO_HEADER: Final[str] = (
    "\n--- Same creator, different region/season (no code changes) ---"
)
