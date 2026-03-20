# Python Code Review Guide

## For Reviewers New to Python

This guide is designed to help reviewers unfamiliar with Python understand the
language constructs, conventions, and design patterns used in this codebase.
It covers Python fundamentals, PEP 8 style rules, and maps every concept
directly to real code from the project so you can review with confidence.

---

## Table of Contents

1. [How to Run the Project](#1-how-to-run-the-project)
2. [Project Structure Overview](#2-project-structure-overview)
3. [Python Language Basics](#3-python-language-basics)
4. [PEP 8 Style Guide (Key Rules)](#4-pep-8-style-guide-key-rules)
5. [Object-Oriented Programming in Python](#5-object-oriented-programming-in-python)
6. [Design Patterns Used](#6-design-patterns-used)
7. [Python-Specific Constructs in the Code](#7-python-specific-constructs-in-the-code)
8. [File-by-File Review Reference](#8-file-by-file-review-reference)
9. [Review Checklist](#9-review-checklist)

---

## 1. How to Run the Project

```bash
# Navigate to the project root directory
cd ITT_Learn_and_Code

# Run the application (requires Python 3.7+)
python main.py
```

No external packages are needed — the project uses only the Python standard library.

---

## 2. Common Python Project Structure

Python projects typically organize code into well-defined folders. Below is a
generic layout you may encounter in **any** Python codebase. Not every project
will have all of these, but these are the most common folders and their purposes.

```
my_project/
├── main.py  OR  app.py               # Entry point — starts the application
├── requirements.txt                   # Lists external packages and versions
├── setup.py  OR  pyproject.toml       # Package/build configuration
├── README.md                          # Project documentation
├── .gitignore                         # Files/folders Git should ignore
├── .env                               # Environment variables (never commit)
│
├── src/  OR  <project_name>/          # Main source code package
│   ├── __init__.py
│   │
│   ├── config/                        # Configuration & settings
│   │   ├── __init__.py
│   │   ├── settings.py                # App settings, env var loading
│   │   └── constants.py               # Fixed values, magic numbers extracted
│   │
│   ├── models/  OR  domain/           # Data models / domain entities
│   │   ├── __init__.py
│   │   ├── user.py                    # Example: User class/dataclass
│   │   └── order.py                   # Example: Order class/dataclass
│   │
│   ├── schemas/                       # Data validation / serialization shapes
│   │   ├── __init__.py
│   │   ├── user_schema.py             # Input/output data shape definitions
│   │   └── order_schema.py
│   │
│   ├── services/  OR  core/           # Business logic / orchestration
│   │   ├── __init__.py
│   │   ├── auth_service.py            # Example: authentication logic
│   │   └── payment_service.py         # Example: payment processing
│   │
│   ├── utils/  OR  helpers/           # Reusable utility functions
│   │   ├── __init__.py
│   │   ├── string_utils.py            # String manipulation helpers
│   │   ├── date_utils.py              # Date/time helpers
│   │   └── file_utils.py              # File I/O helpers
│   │
│   ├── tools/                         # Standalone scripts / CLI tools
│   │   ├── __init__.py
│   │   ├── data_importer.py           # Example: one-off import script
│   │   └── report_generator.py        # Example: report generation tool
│   │
│   ├── api/  OR  routes/              # API endpoints / route handlers
│   │   ├── __init__.py
│   │   ├── user_routes.py
│   │   └── order_routes.py
│   │
│   ├── db/  OR  repositories/         # Database access layer
│   │   ├── __init__.py
│   │   ├── connection.py              # DB connection setup
│   │   └── user_repository.py         # CRUD operations for users
│   │
│   ├── middleware/                     # Request/response middleware
│   │   ├── __init__.py
│   │   └── auth_middleware.py
│   │
│   └── exceptions/                    # Custom exception classes
│       ├── __init__.py
│       └── custom_errors.py
│
├── tests/                             # All test files
│   ├── __init__.py
│   ├── test_user.py
│   └── test_order.py
│
├── docs/                              # Documentation files
├── scripts/                           # Deployment/build/setup scripts
└── data/                              # Sample data, fixtures, seeds
```

### Common Folder Purposes at a Glance

| Folder | What Goes Here |
|--------|----------------|
| **config/** | Settings, constants, environment variable loading, feature flags. No business logic. |
| **models/** (or **domain/**) | Data classes, domain entities, ORM models. These represent the "things" in the system (User, Order, Record, etc.). |
| **schemas/** | Input/output shape definitions for validation and serialization (e.g., Pydantic models, Marshmallow schemas). Defines what data looks like coming in and going out. |
| **services/** (or **core/**) | Business logic and orchestration. Where the main "work" happens. Services coordinate between models, repositories, and external APIs. |
| **utils/** (or **helpers/**) | Small, reusable helper functions that don't belong to any specific domain. String formatting, date calculations, file I/O wrappers, etc. |
| **tools/** | Standalone scripts, CLI commands, one-off tasks. Things you run directly rather than import. |
| **api/** (or **routes/**) | HTTP route handlers, REST endpoints, GraphQL resolvers. The "front door" of a web application. |
| **db/** (or **repositories/**) | Database connection setup, query builders, repository classes that abstract raw SQL/ORM calls. |
| **middleware/** | Code that runs before/after request handling (authentication checks, logging, rate limiting). |
| **exceptions/** | Custom error/exception classes for the project. |
| **tests/** | Unit tests, integration tests, fixtures. Usually mirrors the source folder structure. |
| **docs/** | Project documentation, architecture diagrams, API references. |
| **scripts/** | Shell scripts, deployment automation, CI/CD helpers. |
| **data/** | Sample data files, test fixtures, seed data. |

### What is `__init__.py`?

Every folder containing `__init__.py` is a **Python package**. This file can be
empty or contain re-exports.

If `__init__.py` re-exports classes, it makes imports cleaner:

```python
# Without re-export (long path)
from my_project.models.user import User

# With re-export in models/__init__.py (shorter)
from my_project.models import User
```

The `__init__.py` for the above would contain:
```python
from my_project.models.user import User
```

### Models vs Schemas — What is the Difference?

This distinction confuses many reviewers, so here is a clear breakdown:

**models/** = Internal data representation — how the application stores and
works with data internally. Often maps to database tables.

```python
class User:
    def __init__(self, id, name, email, password_hash):
        self.id = id
        self.name = name
        self.email = email
        self.password_hash = password_hash  # internal only
```

**schemas/** = External data shape — what the API accepts/returns. Defines
validation rules and what fields are exposed to the outside world.

```python
class UserCreateSchema:
    name: str          # required
    email: str         # required
    password: str      # plain text in, never returned

class UserResponseSchema:
    id: int
    name: str
    email: str         # password_hash is NEVER exposed
```

Key differences:
- **models/** may contain sensitive fields (password_hash, internal IDs)
- **schemas/** control what the outside world can send and receive
- A single model can have multiple schemas (create, update, response)

### Utils vs Tools — What is the Difference?

**utils/** = Helper functions you **import** into other code. They are building
blocks, not standalone programs.

```python
# utils/string_utils.py
def slugify(text):
    return text.lower().replace(" ", "-")

# Used as:
from utils.string_utils import slugify
slug = slugify("Hello World")  # "hello-world"
```

**tools/** = Scripts you **run directly** from the command line. They are
standalone programs, not imported by other code.

```python
# tools/data_importer.py
if __name__ == "__main__":
    import_data_from_csv("data.csv")

# Used as:
# python tools/data_importer.py
```

### Services vs Utils — What is the Difference?

- **services/** = Business logic specific to YOUR application.
  "Process a payment", "Register a user", "Generate a report."
  These know about your domain/models.

- **utils/** = Generic helpers that could work in ANY project.
  "Format a date", "Read a file", "Slugify a string."
  These have no knowledge of your specific domain.

---

## 3. Python Language Basics

### 3.1 Indentation Defines Code Blocks

Python uses **indentation** (whitespace) instead of curly braces `{}` to define
code blocks. The standard is **4 spaces** per level.

```python
# Correct - 4 spaces
class MyClass:
    def my_method(self):
        if True:
            print("indented correctly")

# WRONG - inconsistent indentation will cause a SyntaxError
class MyClass:
  def my_method(self):
      if True:
       print("broken")
```

### 3.2 Variables and Types

Python is **dynamically typed** — you do not declare variable types explicitly
(though type hints are supported). Variables are created by assignment.

```python
name = "Alice"        # str (string)
value = 42            # int (integer)
price = 3.14          # float (decimal)
is_valid = True       # bool (boolean)
items = [1, 2, 3]     # list
data = {"key": "val"} # dict (dictionary / hash map)
```

### 3.3 Functions

Functions are defined with the `def` keyword. Parameters can have default values.

```python
# From this project - processor_config.py
def __init__(self,
                validate=DEFAULT_VALIDATE,
                transform=DEFAULT_TRANSFORM,
                date_format=DEFAULT_DATE_FORMAT,
                batch_size=DEFAULT_BATCH_SIZE):
    self.validate = validate
    self.transform = transform
```

- `validate=DEFAULT_VALIDATE` means `validate` has a **default value**;
  callers can omit it.
- Python uses `return` to return values (same as most languages).

### 3.4 The `self` Parameter

In Python, every instance method must take `self` as its **first parameter**.
`self` refers to the current object instance (equivalent to `this` in C#/Java/JS).

```python
class Record:
    def __init__(self, record_id, name, value):
        self._record_id = record_id   # "self." stores it on the instance
        self._name = name

    def capitalize_name(self):         # self is always first
        self._name = self._name.upper()
```

### 3.5 Import System

Python uses `import` statements to bring in code from other modules/packages.

```python
# Import an entire module
import json
import random

# Import specific items from a module
from datetime import datetime, timedelta

# Import from project packages (absolute import)
from data_processing_system.config.constants import DOUBLE_MULTIPLIER
from data_processing_system.domain.record import Record
```

### 3.6 String Formatting (f-strings)

Python 3.6+ supports **f-strings** — string literals prefixed with `f` that
allow embedding expressions inside `{}`.

```python
# From sample_data_generator.py
record_id = f"ID{index:04d}"          # "ID0001", "ID0002", etc.

# From record.py
def __repr__(self):
    return (
        f"Record(record_id={self._record_id}, "
        f"name={self._name}, value={self._value})"
    )
```

- `{index:04d}` means: format `index` as a decimal with 4 digits, zero-padded.
- Any valid Python expression can go inside `{}`.

### 3.7 None (Null Equivalent)

`None` is Python's equivalent of `null` / `nil`. It represents the absence of
a value.

```python
self._doubled_value = None   # No value yet

if record.value is None:     # Check for None using "is", not "=="
    return False
```

### 3.8 Boolean Values

Python booleans are `True` and `False` (capitalized). Logical operators are
English words: `and`, `or`, `not`.

```python
if not record.record_id:    # "not" is the negation operator
    return False
```

### 3.9 Truthiness

In Python, the following values are considered **falsy** (evaluate to `False`):
- `None`, `False`, `0`, `0.0`
- Empty string `""`, empty list `[]`, empty dict `{}`

Everything else is **truthy**. This is why `if not record.record_id:` works
to check for empty or missing values.

---

## 4. PEP 8 Style Guide (Key Rules)

**PEP 8** is the official Python style guide (https://peps.python.org/pep-0008/).
Below are the key rules relevant to reviewing this codebase.

### 4.1 Naming Conventions

| Element         | Convention                | Example from Codebase         |
|-----------------|---------------------------|-------------------------------|
| **Modules**     | `lowercase_with_underscores` | `record_parser.py`, `file_reader.py` |
| **Packages**    | `lowercase` (short)      | `config`, `domain`, `utils`   |
| **Classes**     | `CapitalizedWords` (PascalCase) | `RecordParser`, `JsonExporter` |
| **Functions/Methods** | `lowercase_with_underscores` | `read_lines()`, `filter_min()` |
| **Constants**   | `UPPER_CASE_WITH_UNDERSCORES` | `DOUBLE_MULTIPLIER`, `MAX_VALUE` |
| **Instance variables** | `lowercase_with_underscores` | `self.total_records` |
| **Private attributes** | `_single_leading_underscore` | `self._record_id`, `self._name` |

### 4.2 Indentation

- Use **4 spaces** per indentation level (never tabs).
- Continuation lines should be aligned or use hanging indent.

### 4.3 Maximum Line Length

- Code lines: **79 characters** max (some teams allow up to 99).
- Comments/docstrings: **72 characters** max.

### 4.4 Blank Lines

- **2 blank lines** before and after top-level function/class definitions.
- **1 blank line** between methods inside a class.

### 4.5 Imports

- Imports go at the **top of the file**.
- Each import on its own line (except: `from X import A, B` is fine).
- Group imports in order: (1) standard library, (2) third party, (3) local.
- Use **absolute imports** (this project does this correctly).

### 4.6 Whitespace Rules

```python
# CORRECT
spam(ham[1], {eggs: 2})        # No spaces inside brackets
x = 1                          # Spaces around =
if x == 4:                     # Spaces around ==

# WRONG
spam( ham[ 1 ], { eggs: 2 } )  # Extra spaces inside brackets
x=1                            # Missing spaces around =
```

### 4.7 String Quotes

PEP 8 does not mandate single vs. double quotes, but says: **pick one and be
consistent**. This project consistently uses **double quotes** `"..."`.

---

## 5. Object-Oriented Programming in Python

### 5.1 Classes and `__init__` (Constructor)

`__init__` is Python's constructor. It is called automatically when you create
an object.

```python
# Defining a class (from processor_config.py)
class ProcessorConfig:
    def __init__(self, validate=True, transform=True,
                    date_format="%Y-%m-%d", batch_size=100):
        self.validate = validate
        self.transform = transform
        self.date_format = date_format
        self.batch_size = batch_size

# Creating an instance
config = ProcessorConfig(validate=True, transform=True)
```

### 5.2 Properties (Getters)

The `@property` decorator creates **read-only attributes**. The underlying data
is stored in a private variable (prefixed with `_`), and the property provides
controlled access.

```python
# From record.py
class Record:
    def __init__(self, record_id, name, value, date=None):
        self._record_id = record_id   # Private (convention, not enforced)
        self._name = name

    @property
    def record_id(self):              # Getter - accessed as record.record_id
        return self._record_id

    @property
    def name(self):                   # Getter - accessed as record.name
        return self._name
```

Usage:
```python
record = Record("ID001", "Alice", 100)
print(record.name)        # "Alice"  (calls the @property getter)
record.name = "Bob"       # ERROR - no setter defined, so it's read-only
```

### 5.3 Dunder (Magic/Special) Methods

Methods with double underscores on both sides (`__name__`) are **special
methods** that Python calls automatically in certain contexts.

| Method       | Purpose                                | When Called               |
|--------------|----------------------------------------|---------------------------|
| `__init__`   | Constructor                            | `MyClass()`               |
| `__repr__`   | Official string representation         | `print(obj)`, debugging   |
| `__str__`    | User-friendly string representation    | `str(obj)`, `print(obj)`  |
| `__len__`    | Length of object                       | `len(obj)`                |

```python
# From record.py
def __repr__(self):
    return (
        f"Record(record_id={self._record_id}, "
        f"name={self._name}, value={self._value})"
    )
```

### 5.4 Abstract Base Classes (Interfaces)

Python uses `abc.ABC` and `@abstractmethod` to define interfaces/abstract classes.
Subclasses **must** implement all abstract methods.

```python
# From exporter.py - this is the interface
from abc import ABC, abstractmethod

class Exporter(ABC):
    @abstractmethod
    def export(self, records, file_path):
        pass

# From json_exporter.py - this implements the interface
class JsonExporter(Exporter):
    def export(self, records, file_path):
        data = [record.to_dict() for record in records]
        with open(file_path, "w", encoding="utf-8") as output_file:
            json.dump(data, output_file, indent=JSON_INDENT)
```

If `JsonExporter` did not implement `export()`, Python would raise a
`TypeError` when trying to create an instance.

### 5.5 Inheritance

```python
# Base class (abstract)
class Exporter(ABC):
    @abstractmethod
    def export(self, records, file_path):
        pass

# Derived classes
class JsonExporter(Exporter):  # JsonExporter inherits from Exporter
    def export(self, records, file_path):
        # ... JSON-specific implementation

class XmlExporter(Exporter):   # XmlExporter inherits from Exporter
    def export(self, records, file_path):
        # ... XML-specific implementation

class CsvExporter(Exporter):   # CsvExporter inherits from Exporter
    def export(self, records, file_path):
        # ... CSV-specific implementation
```

The syntax `class Child(Parent):` indicates inheritance.

### 5.6 Encapsulation (Private by Convention)

Python does not have `private` or `protected` keywords. Instead:

| Prefix        | Meaning                    | Enforcement |
|---------------|----------------------------|-------------|
| `name`        | Public                     | Accessible by anyone |
| `_name`       | Private by convention      | "Please don't touch" — not enforced |
| `__name`      | Name-mangled private       | Harder to access from outside |

This project uses single underscore (`_name`) for private attributes in `Record`.

---

## 6. Design Patterns Used

### 6.1 Strategy Pattern (Exporters)

The `Exporter` abstract base class defines an interface. Concrete
implementations (`JsonExporter`, `XmlExporter`, `CsvExporter`) provide
different behaviors. The caller can swap strategies without changing code.

```
Exporter (ABC)           <-- Interface
  ├── JsonExporter       <-- Concrete strategy
  ├── XmlExporter        <-- Concrete strategy
  └── CsvExporter        <-- Concrete strategy
```

### 6.2 Dependency Injection (Constructor Injection)

`DataProcessingService` receives all its dependencies through its constructor
rather than creating them internally. This makes it testable and loosely coupled.

```python
class DataProcessingService:
    def __init__(self, reader, parser, validator, transformer,
                    statistics_calculator, exporter, config):
        self.reader = reader
        self.parser = parser
        # ... all dependencies injected
```

### 6.3 Single Responsibility Principle

Each class has one job:

| Class                  | Responsibility                          |
|------------------------|-----------------------------------------|
| `FileReader`           | Read text files                         |
| `RecordParser`         | Parse CSV lines into Record objects     |
| `RecordValidator`      | Validate records                        |
| `RecordTransformer`    | Apply transformations to records        |
| `StatisticsCalculator` | Compute statistics                      |
| `JsonExporter`         | Export records to JSON format           |
| `ValueFilter`          | Filter records by value                 |
| `Logger`               | Log messages to a file                  |

### 6.4 Orchestrator Pattern

`DataProcessingService.process()` coordinates the entire pipeline:

```
Read file -> Parse records -> Validate -> Transform -> Calculate stats -> Export
```

---

## 7. Python-Specific Constructs in the Code

### 7.1 List Comprehensions

A concise way to create lists by transforming/filtering another iterable.

```python
# Syntax: [expression for item in iterable if condition]

# From file_reader.py - read and strip all non-empty lines
return [line.strip() for line in file if line.strip()]

# From value_filter.py - keep records above minimum value
return [record for record in records if record.value >= min_value]

# From json_exporter.py - convert all records to dicts
data = [record.to_dict() for record in records]

# From data_processing_service.py - filter valid records
records = [record for record in records if self.validator.is_valid(record)]
```

**Equivalent in traditional loop form:**
```python
# This list comprehension:
data = [record.to_dict() for record in records]

# Is equivalent to:
data = []
for record in records:
    data.append(record.to_dict())
```

### 7.2 Generator Expressions

Like list comprehensions but use `()` instead of `[]`. They produce values
lazily (one at a time) instead of building the entire list in memory.

```python
# From statistics_calculator.py
total_value = sum(record.value for record in records)
```

This iterates through records and sums their values without creating an
intermediate list.

### 7.3 Context Managers (`with` statement)

The `with` statement ensures resources are properly cleaned up (e.g., files
are closed) even if an error occurs. Equivalent to try-finally.

```python
# From file_reader.py
with open(file_path, "r", encoding="utf-8") as file:
    return [line.strip() for line in file if line.strip()]
# file is automatically closed here, even if an exception occurred
```

**`open()` parameters explained:**
- First arg: file path
- `"r"` = read mode, `"w"` = write mode
- `encoding="utf-8"` = character encoding

### 7.4 The `if __name__ == "__main__":` Guard

```python
# From main.py
if __name__ == "__main__":
    main()
```

This is a Python idiom. When you run `python main.py`, Python sets the special
variable `__name__` to `"__main__"` for that file. This guard ensures `main()`
only runs when the file is executed directly, not when it is imported by another
module.

### 7.5 Ternary Conditional Expression

```python
# From statistics_calculator.py
average_value = int(total_value / record_count) if record_count > 0 else 0
```

**Syntax:** `value_if_true if condition else value_if_false`

This is equivalent to:
```python
if record_count > 0:
    average_value = int(total_value / record_count)
else:
    average_value = 0
```

### 7.6 Dictionary `.items()` Iteration

```python
# From xml_exporter.py
for field_name, field_value in record.to_dict().items():
    output_file.write(f"    <{field_name}>{field_value}</{field_name}>\n")
```

`.items()` returns key-value pairs from a dictionary. The `for` loop
**unpacks** each pair into two variables (`field_name`, `field_value`).

### 7.7 Constants Module

Python does not have a built-in `const` keyword. By convention, constants
are defined as module-level variables in `UPPER_CASE`.

```python
# From constants.py
DOUBLE_MULTIPLIER = 2
SQUARE_EXPONENT = 2
DEFAULT_BATCH_SIZE = 100
MAX_VALUE = 1000
```

Nothing prevents reassignment, but the naming convention signals "do not modify."

---

## 8. File-by-File Review Reference

### `main.py` — Entry Point

| What to Check | Details |
|----------------|---------|
| Flow | Generates sample data, builds config/service, runs pipeline, exports, filters, displays |
| Functions | `create_processing_config()`, `build_processing_service()`, `display_results()`, `main()` |
| Pattern | Dependency injection — all components assembled here and passed to `DataProcessingService` |

### `config/constants.py` — Constants

| What to Check | Details |
|----------------|---------|
| Convention | All names in `UPPER_CASE_WITH_UNDERSCORES` |
| Purpose | No magic numbers/strings scattered in code; everything centralized |

### `config/processor_config.py` — Configuration Class

| What to Check | Details |
|----------------|---------|
| Pattern | Configuration object with default values from constants |
| Convention | Clean constructor with `self.attribute = parameter` pattern |

### `domain/record.py` — Core Data Entity

| What to Check | Details |
|----------------|---------|
| Properties | `@property` decorators for read-only access to private `_` attributes |
| Methods | `capitalize_name()`, `format_date()`, `compute_derived_values()`, `to_dict()`, `to_csv_row()` |
| Special method | `__repr__` for string representation |
| Encapsulation | Private attributes with `_` prefix |

### `domain/processing_statistics.py` — Statistics Data Object

| What to Check | Details |
|----------------|---------|
| Pattern | Simple data holder with `__repr__` |
| Default | `error_count=0` as default parameter |

### `core/services/data_processing_service.py` — Orchestrator

| What to Check | Details |
|----------------|---------|
| Pattern | Dependency injection via constructor, orchestrator/pipeline pattern |
| Flow | Read -> Parse -> (Validate) -> (Transform) -> Statistics -> Export |
| Feature | Conditional validation and transformation based on config flags |

### `core/transformation/record_transformer.py` — Transformer

| What to Check | Details |
|----------------|---------|
| Pattern | Iterates records and applies three transformations in sequence |
| Note | Modifies records in-place and also returns them |

### `statistics/statistics_calculator.py` — Statistics

| What to Check | Details |
|----------------|---------|
| Feature | Generator expression: `sum(record.value for record in records)` |
| Safety | Division-by-zero guard: `if record_count > 0 else 0` |

### `utils/exporters/exporter.py` — Abstract Interface

| What to Check | Details |
|----------------|---------|
| Pattern | Abstract Base Class (`ABC`) with `@abstractmethod` |
| Purpose | Forces all exporters to implement `export(records, file_path)` |

### `utils/exporters/json_exporter.py`, `xml_exporter.py`, `csv_exporter.py`

| What to Check | Details |
|----------------|---------|
| Pattern | Strategy pattern — each implements `Exporter.export()` differently |
| Feature | Context managers (`with open(...)`) for safe file handling |

### `utils/io/file_reader.py` — File Reader

| What to Check | Details |
|----------------|---------|
| Feature | List comprehension with filtering: `[line.strip() for line in file if line.strip()]` |

### `utils/io/file_writer.py` — File Writer

| What to Check | Details |
|----------------|---------|
| Feature | Context manager for safe file writing |

### `utils/io/sample_data_generator.py` — Test Data Generator

| What to Check | Details |
|----------------|---------|
| Libraries | `random`, `datetime`, `timedelta` (all standard library) |
| Feature | f-string formatting: `f"ID{index:04d}"` |

### `utils/parsing/record_parser.py` — CSV Parser

| What to Check | Details |
|----------------|---------|
| Logic | Splits CSV lines, skips malformed rows (< 3 fields), creates `Record` objects |
| Feature | Conditional expression for optional date field |

### `utils/validation/record_validator.py` — Validator

| What to Check | Details |
|----------------|---------|
| Logic | Checks for empty/missing `record_id`, `name`, and `None` value |
| Style | Early return pattern for validation |

### `utils/filtering/value_filter.py` — Filter

| What to Check | Details |
|----------------|---------|
| Feature | Single-line list comprehension for filtering |

### `utils/logging/logger.py` — Logger

| What to Check | Details |
|----------------|---------|
| Pattern | Buffer pattern — messages stored in list, flushed to file on demand |
| Encapsulation | Private attributes: `_log_file_path`, `_buffer` |

---

## 9. Review Checklist

Use this checklist when reviewing the code:

### Style & Formatting (PEP 8)

- [ ] **Indentation**: Consistent 4 spaces throughout?
- [ ] **Naming**: Classes use `PascalCase`? Functions/methods use `snake_case`? Constants use `UPPER_CASE`?
- [ ] **Imports**: At top of file? Grouped correctly (stdlib, then third-party, then local)?
- [ ] **Line length**: Lines within 79-99 characters?
- [ ] **Blank lines**: 2 blank lines before top-level definitions? 1 blank line between methods?
- [ ] **Quotes**: Consistent use of double quotes?
- [ ] **Whitespace**: No extra spaces inside brackets? Spaces around operators?

### Code Quality

- [ ] **No magic numbers**: All constants in `constants.py`?
- [ ] **Single responsibility**: Each class does one thing?
- [ ] **No code duplication**: Shared logic extracted to common locations?
- [ ] **Meaningful names**: Variables, functions, classes have descriptive names?
- [ ] **Error handling**: Proper checks for `None`, empty values, division by zero?

### Architecture & Design

- [ ] **Dependency injection**: `DataProcessingService` receives dependencies, not creates them?
- [ ] **Strategy pattern**: `Exporter` ABC with concrete implementations?
- [ ] **Encapsulation**: `Record` uses `_private` attributes with `@property` getters?
- [ ] **Separation of concerns**: Config, domain, core logic, utils all separated?
- [ ] **Package structure**: Logical grouping with `__init__.py` re-exports?

### Python Best Practices

- [ ] **Context managers**: `with open(...)` used for all file operations?
- [ ] **List comprehensions**: Used appropriately (readable, not too complex)?
- [ ] **`if __name__ == "__main__"`**: Present in entry point (`main.py`)?
- [ ] **f-strings**: Used consistently for string formatting?
- [ ] **`is None` / `is not None`**: Used instead of `== None` for None checks?

### Data Flow Integrity

- [ ] **Pipeline order**: Read -> Parse -> Validate -> Transform -> Stats -> Export?
- [ ] **Data types**: Values parsed to correct types (e.g., `float(parts[2])`)?
- [ ] **Edge cases**: Empty files, missing fields, zero records handled?

---

## Quick Reference Card

| Python Syntax | Meaning | Equivalent In Other Languages |
|---------------|---------|-------------------------------|
| `def func(self):` | Instance method | `void func()` (C#), `func()` (JS) |
| `self.x = val` | Set instance variable | `this.x = val` |
| `__init__` | Constructor | `constructor()` (JS), `ClassName()` (C#) |
| `@property` | Getter decorator | `get X()` (C#), getter (Java) |
| `@abstractmethod` | Must be overridden | `abstract` (C#/Java) |
| `class A(B):` | A inherits from B | `class A : B` (C#), `class A extends B` (Java) |
| `with open() as f:` | Auto-cleanup file | `using(var f = ...)` (C#), try-with-resources (Java) |
| `[x for x in lst]` | List comprehension | `lst.Select(x => x)` (C# LINQ), `lst.map()` (JS) |
| `if __name__ == "__main__":` | Run only if main | `static void Main()` (C#) |
| `None` | Null value | `null` (C#/Java/JS) |
| `True` / `False` | Boolean | `true` / `false` |
| `and` / `or` / `not` | Logical operators | `&&` / `||` / `!` |
| `f"text {var}"` | String interpolation | `$"text {var}"` (C#), `` `text ${var}` `` (JS) |

---

*Guide generated from codebase analysis and PEP 8 official documentation
(https://peps.python.org/pep-0008/).*
