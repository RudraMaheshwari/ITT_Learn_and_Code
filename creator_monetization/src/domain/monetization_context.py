from __future__ import annotations
from dataclasses import dataclass
from ..utils.validation import (
    require_non_negative_int,
    require_unit_interval,
)

@dataclass(frozen=True, slots=True)
class MonetizationContext:
    views: int
    subscribers: int
    engagement_rate: float
    region: str
    season: str
    live_gift_units: int = 0

    def __post_init__(self) -> None:
        require_non_negative_int("views", self.views)
        require_non_negative_int("subscribers", self.subscribers)
        require_unit_interval("engagement_rate", self.engagement_rate)
        require_non_negative_int("live_gift_units", self.live_gift_units)
        object.__setattr__(self, "region", self.region.strip().upper())
        object.__setattr__(self, "season", self.season.strip().upper())
