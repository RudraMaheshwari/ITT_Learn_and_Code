# Open-Closed Principle (OCP)

The Open-Closed Principle states that software entities (classes, modules, functions) should be open for extension but closed for modification. You should be able to add new functionality without changing existing code.

---

## Files in This Folder

### agent_factory.py

This file demonstrates OCP through its extensible agent creation system. New agents can be added to the factory by simply registering new prompts in the agents dictionary without modifying the core creation logic. The factory pattern allows extending the system with new agent types while the underlying swarm creation mechanism remains unchanged.

---

### base_repository.py

This file follows OCP by providing a robust base class with connection pooling, circuit breaker, and retry logic. New repository implementations can extend this base class to add table-specific functionality without modifying the core connection management code. The resilience patterns are built once and reused across all derived repositories.

---

### exceptions.py

This file adheres to OCP by establishing an exception hierarchy that is open for extension. New exception types can be added by subclassing the base RepositoryException without changing existing exception handling code. Each exception type like ValidationError, DatabaseConnectionError, or RecordNotFoundError extends the base while maintaining compatibility with general exception handlers.

---

### tool_registry.py

This file exemplifies OCP through its registry pattern for managing agent tools. New tools can be registered for any agent by calling the register method without modifying the registry class itself. The simple dictionary-based design allows unlimited extension as new agents and tools are added to the system.
