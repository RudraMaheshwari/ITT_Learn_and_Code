from __future__ import annotations
from abc import ABC
from ..config.constants import (
    MSG_CANNOT_START_NO_FUEL,
    REFUEL_PAST_ACTION,
    REFUEL_QUANTITY_LABEL,
    TEMPLATE_COMBUSTION_VEHICLE_STARTED,
)
from ..core.stored_energy import StoredEnergyPercent
from ..utils.formatting import energy_level_notice_line
from .vehicle import Vehicle

class FuelPoweredVehicle(Vehicle, ABC):
    def __init__(
        self,
        make: str,
        model: str,
        year: int,
        price: float,
        fuel_level_percent: float,
    ) -> None:
        super().__init__(make, model, year, price)
        self._fuel = StoredEnergyPercent(fuel_level_percent)

    @property
    def fuel_level_percent(self) -> float:
        return self._fuel.percent

    def refuel(self, amount_percent: float) -> tuple[str, ...]:
        level = self._fuel.add_percent(amount_percent)
        line = energy_level_notice_line(
            REFUEL_PAST_ACTION, REFUEL_QUANTITY_LABEL, level
        )
        return (line,)

    def start(self) -> tuple[str, ...]:
        started = TEMPLATE_COMBUSTION_VEHICLE_STARTED.format(
            make=self.make, model=self.model
        )
        return self._start_when_energy_available(
            self._fuel.percent,
            MSG_CANNOT_START_NO_FUEL,
            started,
        )
