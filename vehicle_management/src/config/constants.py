from __future__ import annotations

MAX_PRICE_USD: float = 1_000_000
MIN_PRICE_USD: float = 0.0
MAX_STORED_ENERGY_PERCENT: float = 100.0
MIN_STORED_ENERGY_PERCENT: float = 0.0
MIN_ENERGY_DELTA_PERCENT: float = 0.0
EMPTY_ENERGY_THRESHOLD_PERCENT: float = 0.0

PRICE_VALIDATION_ERROR = (
    "Price must be between {min_price:,.0f} and {max_price:,.0f} USD (got {amount})."
)
STORED_ENERGY_VALIDATION_ERROR = (
    "Stored energy must be between 0 and {max_percent:g} percent (got {value})."
)
NEGATIVE_REFUEL_AMOUNT_ERROR = "Added amount cannot be negative."

REGISTRATION_NOTICE_DEFAULT = "Vehicle added"
REGISTRATION_NOTICE_CAR = "Car added"
REGISTRATION_NOTICE_MOTORCYCLE = "Motorcycle added"
REGISTRATION_NOTICE_ELECTRIC_CAR = "Electric car added"

MSG_CANNOT_START_NO_FUEL = "Cannot start - no fuel!"
MSG_CANNOT_START_BATTERY_DEAD = "Cannot start - battery dead!"
TEMPLATE_COMBUSTION_VEHICLE_STARTED = "{make} {model} started."
TEMPLATE_VEHICLE_STOPPED = "{make} {model} stopped."
TEMPLATE_ELECTRIC_VEHICLE_STARTED = "{make} {model} electric motor started."

REFUEL_PAST_ACTION = "Refueled"
REFUEL_QUANTITY_LABEL = "Fuel level"
CHARGE_PAST_ACTION = "Charged"
CHARGE_QUANTITY_LABEL = "Battery level"

ENERGY_LEVEL_NOTICE_TEMPLATE = "{past_action}. {quantity_label}: {level_percent}%"

CAR_SUMMARY_TEMPLATE = "Car: {year} {make} {model}, Price: ${price:,.0f}"
MOTORCYCLE_SUMMARY_TEMPLATE = (
    "Motorcycle: {year} {make} {model}, Sidecar: {has_sidecar}, Price: ${price:,.0f}"
)
ELECTRIC_CAR_SUMMARY_TEMPLATE = (
    "Electric Car: {year} {make} {model}, Price: ${price:,.0f}"
)

INVENTORY_SECTION_HEADER = "\n=== Vehicles ==="

DEMO_TITLE = "=== Vehicle Management Demo ===\n"
DEMO_TESTING_VEHICLES_LABEL = "Testing Vehicles:"
DEMO_TOTAL_VALUE_LABEL = "\nTotal Value: ${value:,.0f}"
DEMO_STARTING_ALL_LABEL = "\nStarting all vehicles:"
DEMO_ENCAPSULATION_SECTION = "\n=== Encapsulation (invalid external mutation) ==="
DEMO_COMPLETE = "\n=== Demo Complete ==="
DEMO_REJECTED_INVALID_PRICE_PREFIX = "Rejected invalid price: {exc}"
DEMO_FUEL_ENCAPSULATION_MESSAGE = (
    "Fuel level cannot be assigned from outside; use refuel() "
    "so invariants stay enforced."
)
DEMO_CAR_PRICE_REMAINS = "Car price remains: ${price:,.0f}"
DEMO_CAR_FUEL_REMAINS = "Car fuel level remains: {fuel_percent:.0f}%"

DEMO_INVALID_PRICE = -1000
DEMO_INVALID_FUEL_ASSIGNMENT_PERCENT = 500

FUEL_LEVEL_PROPERTY_NAME = "fuel_level_percent"

DEMO_CAR_MAKE = "Honda"
DEMO_CAR_MODEL = "Accord"
DEMO_CAR_YEAR = 2023
DEMO_CAR_PRICE = 28_000
DEMO_CAR_FUEL_PERCENT = 100.0

DEMO_MOTORCYCLE_MAKE = "Harley-Davidson"
DEMO_MOTORCYCLE_MODEL = "Street 750"
DEMO_MOTORCYCLE_YEAR = 2022
DEMO_MOTORCYCLE_PRICE = 7_500
DEMO_MOTORCYCLE_FUEL_PERCENT = 80.0
DEMO_MOTORCYCLE_HAS_SIDECAR = False

DEMO_ELECTRIC_MAKE = "Tesla"
DEMO_ELECTRIC_MODEL = "Model 3"
DEMO_ELECTRIC_YEAR = 2023
DEMO_ELECTRIC_PRICE = 42_000
DEMO_ELECTRIC_BATTERY_PERCENT = 100.0

