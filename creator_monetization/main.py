from __future__ import annotations
from src.config import constants as app_constants
from src.domain import (
    AdRevenueStrategy,
    BrandDealStrategy,
    Creator,
    LiveGiftStrategy,
    MonetizationContext,
    SubscriptionStrategy,
)

def _print_breakdown(creator: Creator, context: MonetizationContext) -> None:
    lines = creator.earnings_breakdown(context)
    print(app_constants.DEMO_CREATOR_LABEL.format(name=creator.name))
    print(app_constants.DEMO_SOURCES_HEADER)
    for label, amount in lines:
        print(app_constants.DEMO_SOURCE_LINE.format(label=label, amount=amount))
    print(
        app_constants.DEMO_TOTAL_LINE.format(
            total=sum(amount for _, amount in lines)
        )
    )
    print(app_constants.DEMO_SCENARIO_NOTE)

def _demo_context(*, region: str, season: str) -> MonetizationContext:
    return MonetizationContext(
        views=app_constants.DEMO_VIEWS,
        subscribers=app_constants.DEMO_SUBSCRIBERS,
        engagement_rate=app_constants.DEMO_ENGAGEMENT_RATE,
        region=region,
        season=season,
        live_gift_units=app_constants.DEMO_LIVE_GIFT_UNITS,
    )

def main() -> None:
    print(app_constants.DEMO_TITLE)

    creator = Creator(app_constants.DEMO_CREATOR_DISPLAY_NAME)
    creator.attach_earning_source(AdRevenueStrategy())
    creator.attach_earning_source(SubscriptionStrategy())
    creator.attach_earning_source(
        BrandDealStrategy(contracted_amount=app_constants.DEMO_BRAND_DEAL_AMOUNT)
    )
    creator.attach_earning_source(LiveGiftStrategy())

    _print_breakdown(
        creator,
        _demo_context(
            region=app_constants.DEMO_REGION_PRIMARY,
            season=app_constants.DEMO_SEASON_PRIMARY,
        ),
    )

    print(app_constants.DEMO_SECOND_SCENARIO_HEADER)
    _print_breakdown(
        creator,
        _demo_context(
            region=app_constants.DEMO_REGION_ALT,
            season=app_constants.DEMO_SEASON_ALT,
        ),
    )

if __name__ == "__main__":
    main()
