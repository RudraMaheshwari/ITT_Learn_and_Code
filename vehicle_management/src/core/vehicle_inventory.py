from __future__ import annotations
from ..config.constants import INVENTORY_SECTION_HEADER
from ..domain.vehicle import Vehicle

class VehicleInventory:
    def __init__(self) -> None:
        self._vehicles: list[Vehicle] = []

    def register(self, vehicle: Vehicle) -> None:
        self._vehicles.append(vehicle)

    def registered_vehicles(self) -> tuple[Vehicle, ...]:
        return tuple(self._vehicles)

    def inventory_summary_lines(self) -> tuple[str, ...]:
        body = tuple(v.summary_line() for v in self._vehicles)
        return (INVENTORY_SECTION_HEADER, *body)

    def total_market_value(self) -> float:
        return sum(vehicle.price for vehicle in self._vehicles)

    def start_each_vehicle_notices(self) -> tuple[str, ...]:
        lines: list[str] = []
        for vehicle in self._vehicles:
            lines.extend(vehicle.start())
        return tuple(lines)

