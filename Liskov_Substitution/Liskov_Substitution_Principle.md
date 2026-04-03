# Liskov Substitution Principle (LSP)

The Liskov Substitution Principle states that objects of a superclass should be replaceable with objects of a subclass without affecting the correctness of the program. Derived classes must be substitutable for their base classes.

---

## Files in This Folder

### api_client.py

This file demonstrates LSP through its consistent error handling pattern. The APIClientError exception class and its subtypes can be used interchangeably wherever error handling is expected. All API methods return a consistent dictionary structure with success status, ensuring that callers can reliably process responses regardless of which specific endpoint was called.

---

### base_repository.py

This file follows LSP by providing an abstract base class that defines a contract for all repository implementations. Any class extending BaseRepository can be substituted wherever the base type is expected. The base class establishes consistent methods for query execution, connection handling, and error management that subclasses must honor without altering expected behavior.

---

### lead_tracking_repository.py

This file adheres to LSP by properly extending the repository pattern established by the base class. The LeadTrackingRepository accepts a BaseRepository through composition and uses its connection methods consistently. Any implementation of the base repository can be passed in, and the lead tracking operations will work correctly without modification.

---

### llm_service.py

This file exemplifies LSP by using a factory pattern that returns LLM model instances. The LLMModelProvider wraps the underlying factory and exposes a model property that returns a consistent interface. Any compatible LLM implementation created by the factory can substitute for another, as long as it adheres to the expected language model interface.
