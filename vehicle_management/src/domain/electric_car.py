from __future__ import annotations
from ..config.constants import (
    CHARGE_PAST_ACTION,
    CHARGE_QUANTITY_LABEL,
    ELECTRIC_CAR_SUMMARY_TEMPLATE,
    MSG_CANNOT_START_BATTERY_DEAD,
    REGISTRATION_NOTICE_ELECTRIC_CAR,
    TEMPLATE_ELECTRIC_VEHICLE_STARTED,
)
from ..core.stored_energy import StoredEnergyPercent
from ..utils.formatting import energy_level_notice_line
from .vehicle import Vehicle

class ElectricCar(Vehicle):
    def __init__(
        self,
        make: str,
        model: str,
        year: int,
        price: float,
        battery_percent: float,
    ) -> None:
        super().__init__(make, model, year, price)
        self._battery = StoredEnergyPercent(battery_percent)

    @property
    def battery_percent(self) -> float:
        return self._battery.percent

    def charge(self, amount_percent: float) -> tuple[str, ...]:
        level = self._battery.add_percent(amount_percent)
        line = energy_level_notice_line(
            CHARGE_PAST_ACTION, CHARGE_QUANTITY_LABEL, level
        )
        return (line,)

    def start(self) -> tuple[str, ...]:
        started = TEMPLATE_ELECTRIC_VEHICLE_STARTED.format(
            make=self.make, model=self.model
        )
        return self._start_when_energy_available(
            self._battery.percent,
            MSG_CANNOT_START_BATTERY_DEAD,
            started,
        )

    def registration_notice(self) -> str:
        return REGISTRATION_NOTICE_ELECTRIC_CAR

    def summary_line(self) -> str:
        return ELECTRIC_CAR_SUMMARY_TEMPLATE.format(
            year=self.year,
            make=self.make,
            model=self.model,
            price=self.price,
        )
