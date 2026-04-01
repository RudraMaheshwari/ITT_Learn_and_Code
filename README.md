# ITT_Learn_and_Code

**ITT_Learn_and_Code** is a structured learning and development repository built to help developers understand real-world software concepts through simple, clear, and practical examples.
The goal is to make complex topics easier by demonstrating them with hands-on code, best practices, and explanation-driven learning.

---

## Current Topic — ATM Refactoring: Exceptions vs Error Codes

### The Problem with Error Codes

The original ATM code used integer return codes (`-1`, `-2`, `-3`) to signal failures.
This led to deeply nested `if/else` pyramids where business logic and error handling were completely mixed together.

```python
# Bad — return codes cause nesting and mix logic with error handling
def withdraw(account_id, amount):
    if handle != INVALID:
        if status != DEVICE_SUSPENDED:
            if wifi == WIFI_CONNECTED:
                if balance >= amount:
                    dispense_cash()
                    return SUCCESS
                else:
                    return INSUFFICIENT_FUNDS
            else:
                return CONNECTION_ERROR
        else:
            return DEVICE_SUSPENDED
```

### The Fix — Exceptions + Separated Concerns

Replace return codes with custom exceptions and split business logic from error handling into separate classes.

---

## Project — ATM Withdrawal System

A console-based ATM simulation demonstrating clean exception-based error handling with fully separated business logic.

### How to Run

```bash
python main.py
```

### Folder Structure

```
main.py
src/
    config/
        constants.py            # all constants — zero magic numbers/strings
    core/
        exceptions.py           # custom exceptions
    models/
        account.py              # Account — encapsulated balance, behavior methods
        device.py               # Device — encapsulated status, behavior methods
    services/
        withdrawal_service.py   # business logic — happy path only
    controllers/
        atm_controller.py       # error handling — try/except only
    ui/
        console_menu.py         # console interaction
```

---

## Key Concepts Demonstrated

### 1. Custom Exceptions over Return Codes

```python
# src/core/exceptions.py
class DeviceLockedException(Exception):
    pass

class NetworkConnectionException(Exception):
    pass

class InsufficientFundsException(Exception):
    pass
```

Each failure has its own named exception — intention-revealing, no mental mapping required.

---

### 2. Happy Path — Business Logic Only

`WithdrawalService` reads top-to-bottom like a story. No error handling, no nesting.

```python
def process_withdrawal(self, device, account, amount):
    self.validate_device_is_active(device)
    self.validate_network_connection(device)
    self.validate_sufficient_funds(account, amount)
    self.dispense_cash(account, amount)
```

Each validation raises its own exception if it fails — the method itself never branches.

---

### 3. Error Handling Isolated in Controller

`AtmController` contains all `try/except` logic. Zero business logic lives here.

```python
def withdraw(self, device, account, amount):
    try:
        self.withdrawal_service.process_withdrawal(device, account, amount)
        print(MSG_WITHDRAWAL_SUCCESS)
    except DeviceLockedException:
        print(MSG_DEVICE_LOCKED)
    except NetworkConnectionException:
        print(MSG_NO_CONNECTION)
    except InsufficientFundsException:
        print(MSG_INSUFFICIENT_FUNDS)
```

---

### 4. Encapsulation — Tell, Don't Ask

`Account` and `Device` hide their internal state and expose behavior, not raw data.

```python
# Account — balance is private, behavior is public
account.has_sufficient_funds(amount)   # not: account.balance >= amount
account.deduct(amount)
account.formatted_balance()

# Device — status is private, behavior is public
device.is_active()                     # not: device.status == "ACTIVE"
device.is_connected()
```

---

## Before vs After

| Bad (Error Codes) | Clean (Exceptions) |
|---|---|
| Returns `-1`, `-2`, `-3` | Raises named exceptions |
| 4-level nested `if/else` | Flat, sequential happy path |
| Logic and errors mixed in one method | `WithdrawalService` = logic, `AtmController` = errors |
| Caller must check every return value | Caller catches only what it needs |
| Magic numbers scattered in code | All constants in `src/config/constants.py` |

---

## Clean Code Principles Applied

- **Meaningful names** — `validate_device_is_active`, `has_sufficient_funds`, `is_connected`
- **No magic numbers** — all literals in `src/config/constants.py`
- **Single responsibility** — each class has exactly one job
- **Small functions** — every method does one thing
- **Tell-Don't-Ask** — objects act on their own data
- **Law of Demeter** — no train wrecks, no deep chaining
- **No comments** — naming makes intent obvious

---

## 🚀 What This Repository Offers

- **Real-world coding examples**
- **Clean and scalable code patterns**
- **Step-by-step explanations for clarity**
- **AI, ML, DevOps, and backend code samples**
- **Best practices for Python, APIs, Docker, and more**

---

### **Learn. Build. Improve. Repeat.**
**ITT_Learn_and_Code**
