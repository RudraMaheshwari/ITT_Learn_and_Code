from ..config.constants import CAR_SUMMARY_TEMPLATE, REGISTRATION_NOTICE_CAR
from .fuel_powered_vehicle import FuelPoweredVehicle

class Car(FuelPoweredVehicle):
    def registration_notice(self) -> str:
        return REGISTRATION_NOTICE_CAR

    def summary_line(self) -> str:
        return CAR_SUMMARY_TEMPLATE.format(
            year=self.year,
            make=self.make,
            model=self.model,
            price=self.price,
        )

