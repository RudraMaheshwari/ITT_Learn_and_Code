# Single Responsibility Principle (SRP)

The Single Responsibility Principle states that a class should have only one reason to change. Each module or class should be responsible for a single part of the functionality provided by the software, and that responsibility should be entirely encapsulated by the class.

---

## Files in This Folder

### calendly_status_repository.py

This file demonstrates SRP by focusing exclusively on database operations related to Calendly invite statuses. The class handles only the persistence layer for Calendly data, including creating invite records and retrieving status information. It does not handle Calendly API calls, email notifications, or any business logic outside of data storage and retrieval. If the database schema for Calendly statuses changes, this is the only file that needs modification.

---

### call_session_repository.py

This file follows SRP by managing only the call session data in the database. The class is responsible for creating, updating, and retrieving call session records, including session metadata, transcripts, and call statuses. It does not handle the actual phone call logic, Twilio API integration, or any real-time call processing. The sole responsibility is persisting and querying call session data, making it easy to modify if the database structure for call sessions evolves.

---

### email_service.py

This file adheres to SRP by handling only the task of sending emails through a Logic App webhook. The class validates email formats, prepares payloads, and manages HTTP communication with the external service. It does not manage email templates, track email delivery status in a database, or handle any user interface concerns. If the email sending mechanism changes or a different email provider is used, only this file requires updates.

---

### transcript_extractor.py

This file exemplifies SRP by focusing solely on extracting structured information from conversation transcripts using an LLM. The class takes raw transcript data, formats it appropriately, and uses a language model to extract key conversation details like intent, objections, and contact information. It does not store the extracted data, manage conversations, or handle any call flow logic. When extraction requirements change or the LLM model is updated, modifications are isolated to this single file.
