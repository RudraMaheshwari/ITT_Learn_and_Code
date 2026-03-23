from ..config.constants import (
    MAX_PRICE_USD,
    MAX_STORED_ENERGY_PERCENT,
    MIN_PRICE_USD,
    MIN_ENERGY_DELTA_PERCENT,
    MIN_STORED_ENERGY_PERCENT,
    NEGATIVE_REFUEL_AMOUNT_ERROR,
    PRICE_VALIDATION_ERROR,
    STORED_ENERGY_VALIDATION_ERROR,
)

def validated_price(amount: float) -> float:
    if amount < MIN_PRICE_USD or amount > MAX_PRICE_USD:
        raise ValueError(
            PRICE_VALIDATION_ERROR.format(
                min_price=MIN_PRICE_USD,
                max_price=MAX_PRICE_USD,
                amount=amount,
            )
        )
    return amount

def validated_stored_energy_percent(value: float) -> float:
    if value < MIN_STORED_ENERGY_PERCENT or value > MAX_STORED_ENERGY_PERCENT:
        raise ValueError(
            STORED_ENERGY_VALIDATION_ERROR.format(
                max_percent=MAX_STORED_ENERGY_PERCENT,
                value=value,
            )
        )
    return value

def percent_after_increase(current_percent: float, added_percent: float) -> float:
    if added_percent < MIN_ENERGY_DELTA_PERCENT:
        raise ValueError(NEGATIVE_REFUEL_AMOUNT_ERROR)
    combined = current_percent + added_percent
    return min(combined, MAX_STORED_ENERGY_PERCENT)
