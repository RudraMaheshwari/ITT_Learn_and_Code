from __future__ import annotations
from src.config import constants as app_constants
from src.core.vehicle_inventory import VehicleInventory
from src.domain.car import Car
from src.domain.electric_car import ElectricCar
from src.domain.motorcycle import Motorcycle
from src.domain.vehicle import Vehicle

def _print_lines(lines: tuple[str, ...]) -> None:
    for line in lines:
        print(line)

def _print_blank_line() -> None:
    print()

def _demo_vehicle_followed_by_blank_line(vehicle: Vehicle) -> None:
    _print_lines(vehicle.start())
    print(vehicle.summary_line())
    _print_lines(vehicle.stop())
    _print_blank_line()

def _demo_vehicle_start_and_summary_only(vehicle: Vehicle) -> None:
    _print_lines(vehicle.start())
    print(vehicle.summary_line())

def _register_and_acknowledge(inventory: VehicleInventory, vehicle: Vehicle) -> None:
    inventory.register(vehicle)
    print(vehicle.registration_notice())

def _demonstrate_invalid_price(car: Car) -> None:
    try:
        car.price = app_constants.DEMO_INVALID_PRICE
    except ValueError as exc:
        print(
            app_constants.DEMO_REJECTED_INVALID_PRICE_PREFIX.format(exc=exc)
        )

def _demonstrate_fuel_encapsulation(car: Car) -> None:
    try:
        setattr(car, app_constants.FUEL_LEVEL_PROPERTY_NAME, app_constants.DEMO_INVALID_FUEL_ASSIGNMENT_PERCENT)
    except AttributeError:
        print(app_constants.DEMO_FUEL_ENCAPSULATION_MESSAGE)

def _build_demo_vehicles() -> tuple[Car, Motorcycle, ElectricCar]:
    car = Car(
        make=app_constants.DEMO_CAR_MAKE,
        model=app_constants.DEMO_CAR_MODEL,
        year=app_constants.DEMO_CAR_YEAR,
        price=app_constants.DEMO_CAR_PRICE,
        fuel_level_percent=app_constants.DEMO_CAR_FUEL_PERCENT,
    )
    motorcycle = Motorcycle(
        make=app_constants.DEMO_MOTORCYCLE_MAKE,
        model=app_constants.DEMO_MOTORCYCLE_MODEL,
        year=app_constants.DEMO_MOTORCYCLE_YEAR,
        price=app_constants.DEMO_MOTORCYCLE_PRICE,
        fuel_level_percent=app_constants.DEMO_MOTORCYCLE_FUEL_PERCENT,
        has_sidecar=app_constants.DEMO_MOTORCYCLE_HAS_SIDECAR,
    )
    electric_car = ElectricCar(
        make=app_constants.DEMO_ELECTRIC_MAKE,
        model=app_constants.DEMO_ELECTRIC_MODEL,
        year=app_constants.DEMO_ELECTRIC_YEAR,
        price=app_constants.DEMO_ELECTRIC_PRICE,
        battery_percent=app_constants.DEMO_ELECTRIC_BATTERY_PERCENT,
    )
    return car, motorcycle, electric_car

def main() -> None:
    print(app_constants.DEMO_TITLE)

    car, motorcycle, electric_car = _build_demo_vehicles()

    print(app_constants.DEMO_TESTING_VEHICLES_LABEL)
    _demo_vehicle_followed_by_blank_line(car)
    _demo_vehicle_followed_by_blank_line(motorcycle)
    _demo_vehicle_start_and_summary_only(electric_car)

    inventory = VehicleInventory()
    _register_and_acknowledge(inventory, car)
    _register_and_acknowledge(inventory, motorcycle)
    _register_and_acknowledge(inventory, electric_car)

    _print_lines(inventory.inventory_summary_lines())
    print(
        app_constants.DEMO_TOTAL_VALUE_LABEL.format(
            value=inventory.total_market_value()
        )
    )
    print(app_constants.DEMO_STARTING_ALL_LABEL)
    _print_lines(inventory.start_each_vehicle_notices())

    print(app_constants.DEMO_ENCAPSULATION_SECTION)
    _demonstrate_invalid_price(car)
    _demonstrate_fuel_encapsulation(car)
    print(
        app_constants.DEMO_CAR_PRICE_REMAINS.format(price=car.price)
    )
    print(
        app_constants.DEMO_CAR_FUEL_REMAINS.format(
            fuel_percent=car.fuel_level_percent
        )
    )

    print(app_constants.DEMO_COMPLETE)

if __name__ == "__main__":
    main()

