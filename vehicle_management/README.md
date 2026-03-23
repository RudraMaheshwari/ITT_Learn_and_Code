# Vehicle Management System (Python refactor)

Layered `src/` package: **abstract `Vehicle`**, **fuel vs electric** behavior, **`VehicleInventory`** with one polymorphic list, **constants** for all copy and limits.

## Layout

- `src/config/constants.py` — prices, energy limits, templates, demo data  
- `src/utils/` — `validation.py`, `formatting.py`  
- `src/core/` — `StoredEnergyPercent`, `VehicleInventory`  
- `src/domain/` — `Vehicle`, `FuelPoweredVehicle`, `Car`, `Motorcycle`, `ElectricCar`  

## Run

```bash
python main.py
```

## Assignment mapping

| Issue (original C#) | Approach |
|---------------------|----------|
| Public fields, messy names | Private `_` state; consistent `make` / `model` / `year` |
| Three lists + `is` / casts | Single `list[Vehicle]` + polymorphism |
| Duplicated start/stop/refuel | Shared base + `StoredEnergyPercent` |
| Weak validation | `validated_price`, bounded energy, encapsulation demo in `main` |
| I/O mixed into domain | Domain returns notice strings; `main` prints |
