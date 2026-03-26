from __future__ import annotations

def require_non_negative_int(label: str, value: int) -> None:
    if value < 0:
        raise ValueError(f"{label} cannot be negative (got {value}).")


def require_unit_interval(label: str, value: float) -> None:
    if value < 0.0 or value > 1.0:
        raise ValueError(
            f"{label} must be between 0 and 1 inclusive (got {value})."
        )

def require_non_negative_amount(label: str, value: float) -> None:
    if value < 0.0:
        raise ValueError(f"{label} cannot be negative (got {value}).")

