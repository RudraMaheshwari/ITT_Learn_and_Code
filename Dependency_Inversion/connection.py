"""Database connection management using connection pooling.

This module provides a singleton database connection class that manages
PostgreSQL connections using a thread-safe connection pool.
"""
import psycopg2
from psycopg2.pool import ThreadedConnectionPool
from contextlib import contextmanager
from src.config.settings import get_config
from src.utils.logger import get_logger
from src.database.exceptions import DatabaseConnectionError

config = get_config()
logger = get_logger(__name__)

class DatabaseConnection:
    """Singleton class to manage PostgreSQL database connections using a connection pool."""
    
    _instance = None

    def __new__(cls, *args, **kwargs):
        """Ensure Singleton instance."""
        if cls._instance is None:
            cls._instance = super(DatabaseConnection, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        """Initialize the database connection pool."""
        if hasattr(self, "_initialized") and self._initialized:
            return
        self._pool = None
        self._init_pool()
        self._verify_connection()
        self._initialized = True

    def _init_pool(self):
        """Initialize the connection pool with configuration."""
        try:
            db_config = config.get_postgres_dict()
            self._pool = ThreadedConnectionPool(
                minconn=config.pool_min_connections,
                maxconn=config.pool_max_connections,
                **db_config
            )
            logger.info("Database connection pool initialized")
        except psycopg2.Error as e:
            logger.error(f"Failed to initialize database pool: {e}")
            raise DatabaseConnectionError("Failed to initialize database pool", e)
        except Exception as e:
            logger.error(f"Unexpected error initializing database pool: {e}")
            raise

    @contextmanager
    def get_connection(self):
        """Provide a safe context-managed database connection.
        
        Yields:
            psycopg2 connection object
            
        Raises:
            DatabaseConnectionError: If connection cannot be acquired
        """
        conn = None
        try:
            conn = self._pool.getconn()
            conn.autocommit = True
            yield conn
        except psycopg2.Error as e:
            logger.error(f"Database error during connection usage: {e}")
            raise DatabaseConnectionError("Database operation failed", e)
        except Exception as e:
            logger.error(f"Error during connection usage: {e}")
            raise
        finally:
            if conn:
                try:
                    conn.rollback()
                except Exception as e:
                    logger.warning(f"Error during connection rollback: {e}")
                try:
                    self._pool.putconn(conn)
                except Exception as e:
                    logger.error(f"Error returning connection to pool: {e}")

    def _verify_connection(self):
        """Verify database connectivity without creating tables."""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT 1")
                cursor.close()
            logger.info("Database connection verified and ready")
        except Exception as e:
            logger.error(f"Failed to verify database connection: {e}")
            raise

    def close_all(self):
        """Close all connections in the pool."""
        if self._pool:
            try:
                self._pool.closeall()
                logger.info("All database connections closed")
            except Exception as e:
                logger.error(f"Error closing connection pool: {e}")

    @property
    def pool(self):
        """Get the connection pool (for backward compatibility)."""
        return self._pool

_db_conn_instance = None

def get_db_connection() -> DatabaseConnection:
    """Get the singleton DatabaseConnection instance.
    
    Returns:
        DatabaseConnection: The singleton database connection instance
    """
    global _db_conn_instance
    if _db_conn_instance is None:
        _db_conn_instance = DatabaseConnection()
    return _db_conn_instance
