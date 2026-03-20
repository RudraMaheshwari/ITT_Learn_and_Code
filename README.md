# ITT_Learn_and_Code

Structured learning repo: practical examples, **OOP / SOLID refactors**, and clean coding habits.  
Below are two **OOP Concepts** assignments (original specs in C#); the Python solutions live in subfolders.

| Assignment | Folder | Themes |
|------------|--------|--------|
| Vehicle Management System | [`vehicle_management/`](vehicle_management/) | Encapsulation, inheritance, polymorphism, abstraction, clean structure |
| Creator Monetization Platform | [`creator_monetization/`](creator_monetization/) | Strategy pattern, composition, OCP, multiple revenue streams |

Run demos:

```bash
cd vehicle_management && python main.py
cd creator_monetization && python main.py
```

---

## Assignment 1 — Vehicle Management System (OOP Refactor)

### Problem statement

You are given a **Vehicle Management System** codebase that **violates multiple OOP principles and coding standards**. Your task is to **refactor** it to align with industry best practices.

### Key focus areas

1. Identify and fix violations related to **Encapsulation**, **Inheritance**, **Polymorphism**, and **Abstraction**.
2. Ensure the refactored codebase follows **proper coding standards and best practices**.

### Original codebase (C#) — reference

The starter code includes separate classes (`Car`, `Motorcycle`, `ElectricCar`), a `VehicleManager` with parallel lists and `object` + type checks, public fields, inconsistent naming, duplicated logic, and broken / inconsistent members (e.g. mixed `Start` / `start_engine`, wrong identifiers in some methods).

<details>
<summary><strong>Original C# excerpt (collapse)</strong></summary>

```csharp
public class Car
{
    public string make;
    public string Model;
    public int year_of_manufacture;
    public double Price;
    public double fuel_level;
    public bool is_running;
    public void set_price(double price) { Price = price; /* TODO: validation */ }
    public void start_engine() { /* ... */ }
    public void Stop() { IsRunning = false; /* wrong identifiers */ }
    // ...
}

public class VehicleManager
{
    public List<Car> Cars = new List<Car>();
    public List<Motorcycle> Motorcycles = new List<Motorcycle>();
    public List<ElectricCar> ElectricCars = new List<ElectricCar>();

    public void AddVehicle(object vehicle)
    {
        if (vehicle is Car) { Cars.Add((Car)vehicle); }
        else if (vehicle is Motorcycle) { /* ... */ }
        else if (vehicle is ElectricCar) { /* ... */ }
    }
    // display_all, calc_total_value, start_all_vehicles — each list typed separately
}
```

</details>

### What to fix (checklist)

- Public mutable fields; inconsistent naming (`make` / `Model` / `MAKE`, etc.).
- Duplicated start/stop/refuel patterns; electric vs fuel special cases without a clear model.
- **Single polymorphic collection** instead of three lists + `is` / casts.
- **Encapsulation**: validated price, bounded fuel/battery, no invalid external mutation.
- Uniform **verbs** (`start`, `stop`) and one way to show vehicle info.

### Python solution

See **[`vehicle_management/README.md`](vehicle_management/README.md)** for layout, design mapping, and how the refactor addresses the above.

---

## Assignment 2 — Creator Monetization Platform (Refactoring & Design)

### Problem statement

You are building the **backend logic** for a **Creator Monetization Platform** (similar to Instagram, YouTube, or LinkedIn). Creators earn through multiple dynamic sources:

- Brand deals  
- Ad revenue  
- Subscriptions  
- Live gifts  

The system evolved quickly and suffers from **inconsistent logic**, **duplication**, and **poor extensibility**.

Your task: **refactor and redesign** using **OOP & SOLID** so it **scales with new monetization models**.

### Your tasks

**1. Identify design issues**

- Public mutable fields and **if–else explosion** on earning type.
- **Single** earning type limitation (cannot combine ads + subs + brand).
- **No extensibility**; changes require editing core logic.
- Violates **Open–Closed Principle (OCP)**.

**2. Redesign the system**

- Allow **multiple earning strategies per creator**.
- Support **easy addition** of new earning types.
- **Avoid** `if (type == …)` chains for earnings.
- **Encapsulate** all data properly.
- **Separate** earning logic from the **Creator** entity.

**3. Introduce proper OOP design**

- **Abstraction**
- **Composition over inheritance** (where appropriate)
- **Strategy pattern** (optional but recommended)

**4. Real-world complexity**

- A creator earns from **ads + subscription + brand deals** (and optionally more, e.g. live gifts).
- Some earnings depend on **engagement rate**, **region**, and **season**.

### Original codebase (C#) — reference

<details>
<summary><strong>Original C# excerpt (collapse)</strong></summary>

```csharp
public class Creator
{
    public string name;
    public string earningType;
    public double baseAmount;
    public int views;
    public int subscribers;

    public double CalculateEarnings()
    {
        if (earningType == "ADS")
            return views * 0.05;
        else if (earningType == "SUBSCRIPTION")
            return subscribers * 2;
        else if (earningType == "BRAND")
            return baseAmount;
        return 0;
    }
}
```

</details>

### Python solution

See **[`creator_monetization/README.md`](creator_monetization/README.md)** for layout and how tasks map to code. Base rates match the original snippet when regional/season multipliers are neutral (`0.05` per view, `2` per subscriber, fixed brand amount).

---

## Repository purpose (general)

- One place to **learn and build** with **readable, layered Python** examples.  
- Topics can include APIs, tooling, and patterns; **OOP assignments above** are the current highlighted work.

---

## Who this is for

Students, interview practice, and anyone learning **OOP, SOLID, and clean structure** by reading working code.

---

## Contribution

Pull requests and issues are welcome for new examples or clarifications.

---

**Learn. Build. Improve. Repeat.**
