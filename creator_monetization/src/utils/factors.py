from __future__ import annotations
from ..config.constants import (
    DEFAULT_REGION_KEY,
    DEFAULT_SEASON_KEY,
    REGION_MULTIPLIERS,
    SEASON_MULTIPLIERS,
)

def regional_multiplier(region_code: str) -> float:
    return REGION_MULTIPLIERS.get(
        region_code.upper(), REGION_MULTIPLIERS[DEFAULT_REGION_KEY]
    )

def seasonal_multiplier(season_name: str) -> float:
    return SEASON_MULTIPLIERS.get(
        season_name.upper(), SEASON_MULTIPLIERS[DEFAULT_SEASON_KEY]
    )
