# Interface Segregation Principle (ISP)

The Interface Segregation Principle states that clients should not be forced to depend on interfaces they do not use. It is better to have many small, specific interfaces than one large, general-purpose interface.

---

## Files in This Folder

### dashboard_helpers.py

This file demonstrates ISP by providing small, focused helper functions that dashboards can use selectively. Instead of one massive utility class with all possible dashboard operations, this module offers targeted functions like pagination controls and refresh intervals. Each dashboard imports only what it needs without depending on unrelated functionality.

---

### dependencies.py

This file follows ISP through its ServiceLocator class that exposes specific getter methods for individual services. Rather than forcing clients to accept a monolithic service container, each component can request only the specific service it requires through dedicated methods like get_agent, get_twilio_client, or get_call_session_service.

---

### email_count_dashboard.py

This file adheres to ISP by consuming only the specific interfaces it needs from helper modules and repositories. The dashboard imports only the pagination helpers and repository methods relevant to email tracking, not the entire suite of available functionality. This keeps the module decoupled from unrelated capabilities.

---

### email_service.py

This file exemplifies ISP by providing a focused interface for email operations. The class exposes only the methods needed for sending templated emails, without bundling unrelated concerns like email tracking analytics or user management. Consumers of this service are not burdened with methods they do not need.

---

### jotform_service.py

This file demonstrates ISP by offering a minimal interface for Jotform URL generation and lead ID encryption. The service exposes only the methods required for form integration, such as generating URLs and encrypting tokens. It does not force consumers to depend on unused API operations or form management features.
