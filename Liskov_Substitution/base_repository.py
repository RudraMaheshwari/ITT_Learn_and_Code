"""Base repository with shared database operations.

This module provides a base class with common functionality for
all repository classes, eliminating code duplication and ensuring
consistent cursor/connection lifecycle management.
"""
import json
from abc import ABC
from contextlib import contextmanager
from typing import Any, Dict, List, Optional, Callable, TypeVar

from src.database.connection import get_db_connection
from src.database.exceptions import (
    DatabaseConnectionError,
    QueryExecutionError,
    RepositoryException
)
from src.utils.logger import get_logger

T = TypeVar('T')

class BaseRepository(ABC):
    """Abstract base class for repository implementations.
    
    Provides common database operations and lifecycle management
    to reduce code duplication across repository classes.
    """

    _logger = None

    @classmethod
    def _get_logger(cls):
        """Get or create logger instance for the repository."""
        if cls._logger is None:
            cls._logger = get_logger(cls.__name__)
        return cls._logger

    @classmethod
    @contextmanager
    def _get_cursor(cls):
        """Context manager for safe cursor acquisition and cleanup.
        
        Yields:
            Database cursor
            
        Raises:
            DatabaseConnectionError: If connection fails
        """
        db = get_db_connection()
        cursor = None
        
        try:
            with db.get_connection() as conn:
                cursor = conn.cursor()
                yield cursor, conn
        except Exception as e:
            cls._get_logger().error(f"Database connection error: {e}")
            raise DatabaseConnectionError("Failed to acquire database cursor", e)
        finally:
            if cursor:
                try:
                    cursor.close()
                except Exception:
                    pass

    @classmethod
    def _execute_query(
        cls,
        query: str,
        params: tuple = None,
        operation_name: str = "query"
    ) -> List[tuple]:
        """Execute a query and return all results.
        
        Args:
            query: SQL query string
            params: Query parameters
            operation_name: Name of operation for logging
            
        Returns:
            List of result tuples
            
        Raises:
            QueryExecutionError: If query fails
        """
        try:
            with cls._get_cursor() as (cursor, conn):
                cursor.execute(query, params)
                return cursor.fetchall()
        except DatabaseConnectionError:
            raise
        except Exception as e:
            cls._get_logger().exception(f"Error executing {operation_name}: {e}")
            raise QueryExecutionError(operation_name, e)

    @classmethod
    def _execute_single(
        cls,
        query: str,
        params: tuple = None,
        operation_name: str = "query"
    ) -> Optional[tuple]:
        """Execute a query and return single result.
        
        Args:
            query: SQL query string
            params: Query parameters
            operation_name: Name of operation for logging
            
        Returns:
            Single result tuple or None
            
        Raises:
            QueryExecutionError: If query fails
        """
        try:
            with cls._get_cursor() as (cursor, conn):
                cursor.execute(query, params)
                return cursor.fetchone()
        except DatabaseConnectionError:
            raise
        except Exception as e:
            cls._get_logger().exception(f"Error executing {operation_name}: {e}")
            raise QueryExecutionError(operation_name, e)

    @classmethod
    def _execute_write(
        cls,
        query: str,
        params: tuple = None,
        operation_name: str = "write",
        return_id: bool = False
    ) -> Optional[Any]:
        """Execute a write operation (INSERT/UPDATE/DELETE).
        
        Args:
            query: SQL query string
            params: Query parameters
            operation_name: Name of operation for logging
            return_id: If True, return the first column of result
            
        Returns:
            Returned ID if return_id is True, else row count
            
        Raises:
            QueryExecutionError: If query fails
        """
        try:
            with cls._get_cursor() as (cursor, conn):
                cursor.execute(query, params)
                conn.commit()
                
                if return_id:
                    result = cursor.fetchone()
                    return result[0] if result else None
                
                return cursor.rowcount
        except DatabaseConnectionError:
            raise
        except Exception as e:
            cls._get_logger().exception(f"Error executing {operation_name}: {e}")
            raise QueryExecutionError(operation_name, e)

    @classmethod
    def _execute_count(
        cls,
        query: str,
        params: tuple = None,
        operation_name: str = "count"
    ) -> int:
        """Execute a COUNT query and return the count.
        
        Args:
            query: SQL COUNT query string
            params: Query parameters
            operation_name: Name of operation for logging
            
        Returns:
            Count value
        """
        try:
            result = cls._execute_single(query, params, operation_name)
            return result[0] if result else 0
        except Exception:
            return 0

    @staticmethod
    def _parse_transcript(raw_transcript: Any, call_sid: str, logger) -> Any:
        """Parse transcript data from various formats.
        
        Args:
            raw_transcript: Raw transcript data from database
            call_sid: Call SID for logging context
            logger: Logger instance
            
        Returns:
            Parsed transcript data
        """
        if not raw_transcript:
            return None

        if isinstance(raw_transcript, (dict, list)):
            return raw_transcript

        if isinstance(raw_transcript, memoryview):
            try:
                raw_text = raw_transcript.tobytes().decode("utf-8")
                return json.loads(raw_text)
            except json.JSONDecodeError as e:
                logger.warning(f"Failed to parse transcript JSON for {call_sid}: {e}")
                return raw_text
            except UnicodeDecodeError as e:
                logger.warning(f"Failed to decode transcript for {call_sid}: {e}")
                return str(raw_transcript)

        if isinstance(raw_transcript, str):
            raw_text = raw_transcript.strip()
            try:
                if raw_text.startswith("{") or raw_text.startswith("["):
                    return json.loads(raw_text)
                return raw_text
            except json.JSONDecodeError as e:
                logger.warning(f"Failed to parse transcript JSON for {call_sid}: {e}")
                return raw_text

        return str(raw_transcript)

    @classmethod
    def _safe_execute(
        cls,
        operation: Callable[[], T],
        default: T,
        operation_name: str = "operation"
    ) -> T:
        """Safely execute an operation with fallback to default.
        
        Args:
            operation: Callable to execute
            default: Default value if operation fails
            operation_name: Name of operation for logging
            
        Returns:
            Result of operation or default value
        """
        try:
            return operation()
        except RepositoryException:
            raise
        except Exception as e:
            cls._get_logger().exception(f"Error in {operation_name}: {e}")
            return default
