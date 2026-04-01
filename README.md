# ITT_Learn_and_Code

**ITT_Learn_and_Code** is a structured learning repository that demonstrates real-world software concepts through simple, clean, and practical Python examples.

---

## Current Topic — `try-finally`

### What is `try-finally`?

`try-finally` guarantees that the `finally` block **always runs** — whether the `try` block succeeds or fails.
It is used purely for **cleanup and resource management**, not for error handling.

```python
file = open("expenses.txt", "a+")
try:
    file.seek(0)
    lines = file.readlines()
finally:
    file.close()   # always executes — success or failure
```

### Why `try-finally` and not `try-except-finally`?

| Block | Purpose |
|---|---|
| `try` | Execute the operation |
| `except` | Handle a specific error |
| `finally` | Cleanup — always runs regardless |

When you only need **guaranteed cleanup** and do not want to suppress or handle any error, use `try-finally` alone.
Adding `except` would mean you intend to catch and handle errors — which is a different concern.

---

## Project — Personal Expense Tracker

A console-based application that lets you add, view, and clear expenses stored in a file.
The project showcases `try-finally` for file handle management across all I/O operations.

### How to Run

```bash
python main.py
```

### Folder Structure

```
main.py
src/
    config/
        constants.py        # all constants and string literals
    models/
        expense.py          # Expense data class
    services/
        expense_service.py  # business logic
    storage/
        file_handler.py     # try-finally for file I/O
    ui/
        console_menu.py     # console interaction
```

### Where `try-finally` is Used

| File | Method | Purpose |
|---|---|---|
| `src/storage/file_handler.py` | `read_lines()` | Ensures file closes after reading |
| `src/storage/file_handler.py` | `append_line()` | Ensures file closes after writing |
| `src/storage/file_handler.py` | `clear_contents()` | Ensures file closes after clearing |

All three are in `src/storage/file_handler.py` — the only file in this project that uses `try-finally`.
No other file needs it because resource management is intentionally isolated to `FileHandler`.

**Read**
```python
file = open(EXPENSE_FILE_PATH, FILE_MODE_READ_APPEND)
try:
    file.seek(0)
    lines = file.readlines()
finally:
    file.close()
```

**Write**
```python
file = open(EXPENSE_FILE_PATH, FILE_MODE_APPEND)
try:
    file.write(line + NEWLINE)
finally:
    file.close()
```

**Clear**
```python
file = open(EXPENSE_FILE_PATH, FILE_MODE_WRITE)
try:
    file.write("")
finally:
    file.close()
```

In every case, `file.close()` is guaranteed to run — even if `readlines()` or `write()` raises an exception internally. This prevents file handle leaks.

---

## Clean Code Principles Applied

- **Meaningful names** — `fetch_all_expenses`, `format_for_display`, `is_running`
- **No magic numbers** — all literals live in `src/config/constants.py`
- **Single responsibility** — each class has one job
- **Small functions** — every method does exactly one thing
- **Command/Query separation** — methods either act or return, not both
- **Boolean prefix** — `is_running`
- **Classes as nouns, methods as verbs** — `ExpenseService.add_expense`, `FileHandler.read_lines`

---

### Learn. Build. Improve. Repeat.
