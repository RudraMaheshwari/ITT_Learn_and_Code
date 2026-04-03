# Dependency Inversion Principle (DIP)

The Dependency Inversion Principle states that high-level modules should not depend on low-level modules. Both should depend on abstractions. Additionally, abstractions should not depend on details; details should depend on abstractions.

---

## Files in This Folder

### call_session_service.py

This file demonstrates DIP by accepting a repository instance through its constructor rather than creating one internally. The service layer depends on an abstraction (the repository interface) rather than a concrete database implementation. This allows the repository to be swapped out for testing purposes or if the storage mechanism changes, without modifying the service code itself.

---

### connection.py

This file follows DIP by providing a database connection abstraction that other parts of the application depend upon. The connection pool management is encapsulated behind a simple interface, so consuming code never needs to know the specifics of how connections are created, pooled, or recycled. Changes to the underlying connection logic remain isolated here.

---

### validators.py

This file adheres to DIP by providing reusable validation functions that can be injected or imported wherever input validation is needed. The validators depend on configuration abstractions for pagination settings rather than hardcoded values. Higher-level modules that need validation can rely on these abstractions without coupling themselves to specific validation implementations.
