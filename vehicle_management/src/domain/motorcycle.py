from ..config.constants import (
    MOTORCYCLE_SUMMARY_TEMPLATE,
    REGISTRATION_NOTICE_MOTORCYCLE,
)
from .fuel_powered_vehicle import FuelPoweredVehicle

class Motorcycle(FuelPoweredVehicle):
    def __init__(
        self,
        make: str,
        model: str,
        year: int,
        price: float,
        fuel_level_percent: float,
        has_sidecar: bool = False,
    ) -> None:
        super().__init__(make, model, year, price, fuel_level_percent)
        self._has_sidecar = has_sidecar

    @property
    def has_sidecar(self) -> bool:
        return self._has_sidecar

    def registration_notice(self) -> str:
        return REGISTRATION_NOTICE_MOTORCYCLE

    def summary_line(self) -> str:
        return MOTORCYCLE_SUMMARY_TEMPLATE.format(
            year=self.year,
            make=self.make,
            model=self.model,
            has_sidecar=self._has_sidecar,
            price=self.price,
        )
