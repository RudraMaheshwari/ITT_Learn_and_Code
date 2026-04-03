"""Custom exceptions for database operations.

This module provides a hierarchy of exceptions for handling
database-related errors with appropriate granularity.
"""

class RepositoryException(Exception):
    """Base exception for all repository operations."""

    def __init__(self, message: str, original_error: Exception = None):
        self.message = message
        self.original_error = original_error
        super().__init__(self.message)

    def __str__(self) -> str:
        if self.original_error:
            return f"{self.message} (caused by: {self.original_error})"
        return self.message

class ValidationError(RepositoryException):
    """Raised when input validation fails."""

    def __init__(self, field: str, message: str):
        self.field = field
        super().__init__(f"Validation error on '{field}': {message}")

class DatabaseConnectionError(RepositoryException):
    """Raised when database connection fails."""

    def __init__(self, message: str = "Failed to connect to database", original_error: Exception = None):
        super().__init__(message, original_error)

class RecordNotFoundError(RepositoryException):
    """Raised when a requested record is not found."""

    def __init__(self, entity: str, identifier: str):
        self.entity = entity
        self.identifier = identifier
        super().__init__(f"{entity} with identifier '{identifier}' not found")

class QueryExecutionError(RepositoryException):
    """Raised when a database query fails to execute."""

    def __init__(self, operation: str, original_error: Exception = None):
        self.operation = operation
        super().__init__(f"Failed to execute {operation}", original_error)

class TransactionError(RepositoryException):
    """Raised when a database transaction fails."""

    def __init__(self, message: str = "Transaction failed", original_error: Exception = None):
        super().__init__(message, original_error)
