from datetime import datetime
from typing import Dict, Any
from contextlib import contextmanager
from psycopg2.pool import ThreadedConnectionPool, PoolError
from psycopg2 import OperationalError, InterfaceError, DatabaseError
from tenacity import (
    retry,
    stop_after_attempt,
    wait_exponential,
    retry_if_exception_type,
    RetryError
)
from pybreaker import CircuitBreaker, CircuitBreakerError
from src.utils.logger import logger

class BaseRepository:
    """Base repository class with connection pooling and circuit breaker logic."""
    
    def __init__(self, connection_config: dict, pool_size: int = 10, 
                 max_retry_attempts: int = 3, circuit_breaker_fail_max: int = 5,
                 circuit_breaker_timeout: int = 60):
        """
        Initialize the repository with PostgreSQL connection config.
        
        Args:
            connection_config: PostgreSQL connection parameters
            pool_size: Maximum number of connections in pool
            max_retry_attempts: Maximum retry attempts for transient failures
            circuit_breaker_fail_max: Number of failures before circuit breaker opens
            circuit_breaker_timeout: Seconds before circuit breaker attempts recovery
        """
        self.connection_config = connection_config
        self.pool_size = pool_size
        self.max_retry_attempts = max_retry_attempts
        self.pool = None
        
        self.last_successful_connection = None
        self.failed_connection_attempts = 0
        self.total_connections_acquired = 0
        
        self.db_breaker = CircuitBreaker(
            fail_max=circuit_breaker_fail_max,
            reset_timeout=circuit_breaker_timeout,
            name="postgres_connection"
        )
        
        self._init_pool()
    
    def _on_circuit_breaker_state_change(self, cb, old_state, new_state):
        """Callback for circuit breaker state changes."""
        if old_state != new_state:
            logger.warning(
                f"Database circuit breaker state changed: {old_state} -> {new_state}. "
                f"Failed attempts: {self.failed_connection_attempts}"
            )
    
    def _init_pool(self):
        """Initialize connection pool with validation."""
        try:
            self.pool = ThreadedConnectionPool(
                minconn=1,
                maxconn=self.pool_size,
                **self.connection_config
            )
            logger.info(
                f"PostgreSQL connection pool initialized "
                f"(min=1, max={self.pool_size}, timeout={self.connection_config.get('connect_timeout', 10)}s)"
            )
            
            self._validate_pool_connection()
            logger.info("PostgreSQL connection pool validated successfully")
            
        except (OperationalError, DatabaseError) as e:
            logger.error(f"Failed to initialize connection pool - Database error: {e}")
            self.failed_connection_attempts += 1
            raise ConnectionError(
                f"Cannot connect to PostgreSQL database. Check your database configuration. Error: {e}"
            ) from e
        except Exception as e:
            logger.error(f"Failed to initialize connection pool - Unexpected error: {e}")
            self.failed_connection_attempts += 1
            raise
    
    def _validate_pool_connection(self):
        """Validate that the pool can acquire and use a connection."""
        conn = None
        try:
            conn = self.pool.getconn()
            cursor = conn.cursor()
            cursor.execute("SELECT 1")
            cursor.fetchone()
            cursor.close()
            self.last_successful_connection = datetime.utcnow()
            logger.debug("Connection pool validation successful")
        finally:
            if conn:
                self.pool.putconn(conn)
    
    def _acquire_connection_with_retry(self):
        """
        Acquire connection from pool with retry logic for transient failures.
        
        Uses tenacity to retry on transient database errors with exponential backoff.
        
        Returns:
            Database connection from pool
            
        Raises:
            PoolError: When connection pool is exhausted
            OperationalError: When connection cannot be established
        """
        if str(self.db_breaker.current_state) == 'open':
            raise CircuitBreakerError("Circuit breaker is OPEN")
        
        @retry(
            stop=stop_after_attempt(self.max_retry_attempts),
            wait=wait_exponential(multiplier=1, min=1, max=10),
            retry=retry_if_exception_type((OperationalError, InterfaceError)),
            reraise=True
        )
        def _get_conn():
            try:
                conn = self.pool.getconn()
                if conn is None:
                    raise PoolError("Connection pool returned None")
                
                if conn.closed:
                    logger.warning("Received closed connection from pool, retrying...")
                    self.pool.putconn(conn, close=True)
                    raise InterfaceError("Connection was closed")
                
                return conn
            except PoolError as e:
                logger.error(f"Connection pool exhausted: {e}")
                self.failed_connection_attempts += 1
                raise
        
        try:
            conn = _get_conn()
            try:
                self.db_breaker.call_succeeded()
            except:
                pass
            return conn
        except Exception as e:
            try:
                self.db_breaker.call_failed()
            except:
                pass
            raise
    
    @contextmanager
    def _get_connection(self):
        """
        Context manager for database connections with circuit breaker and retry logic.
        
        Handles:
        - Connection acquisition with retry logic
        - Circuit breaker pattern to prevent cascading failures
        - Automatic rollback on exceptions
        - Proper connection cleanup
        
        Yields:
            Database connection
            
        Raises:
            CircuitBreakerError: When circuit breaker is open
            PoolError: When connection pool is exhausted
            OperationalError: When connection fails after retries
        """
        conn = None
        try:
            conn = self._acquire_connection_with_retry()
            
            self.total_connections_acquired += 1
            self.last_successful_connection = datetime.utcnow()
            self.failed_connection_attempts = 0
            
            yield conn
            
        except CircuitBreakerError as e:
            self.failed_connection_attempts += 1
            logger.error(
                f"Database circuit breaker is OPEN - rejecting connection attempts. "
                f"Failed attempts: {self.failed_connection_attempts}. "
                f"The circuit breaker will attempt recovery after cooldown period."
            )
            raise ConnectionError(
                "Database is currently unavailable due to repeated connection failures. "
                "Please try again later."
            ) from e
        except PoolError as e:
            self.failed_connection_attempts += 1
            logger.error(
                f"Connection pool exhausted (size={self.pool_size}). "
                f"Consider increasing PG_POOL_SIZE or investigating connection leaks."
            )
            raise ConnectionError(
                f"Database connection pool exhausted. All {self.pool_size} connections are in use."
            ) from e
        except RetryError as e:
            self.failed_connection_attempts += 1
            logger.error(
                f"Failed to acquire database connection after {self.max_retry_attempts} attempts. "
                f"Original error: {e.last_attempt.exception()}"
            )
            raise ConnectionError(
                f"Could not connect to database after {self.max_retry_attempts} retry attempts."
            ) from e
        except (OperationalError, InterfaceError, DatabaseError) as e:
            self.failed_connection_attempts += 1
            logger.error(f"Database connection error: {e}")
            raise
        except Exception as e:
            self.failed_connection_attempts += 1
            logger.error(f"Unexpected error acquiring database connection: {e}")
            if conn and not conn.closed:
                try:
                    conn.rollback()
                except Exception as rollback_error:
                    logger.warning(f"Failed to rollback transaction: {rollback_error}")
            raise
        finally:
            if conn:
                try:
                    self.pool.putconn(conn)
                except Exception as e:
                    logger.error(f"Error returning connection to pool: {e}")
    
    def health_check(self) -> Dict[str, Any]:
        """
        Check database connectivity and return pool status.
        
        Returns comprehensive health information about the database connection:
        - Circuit breaker state (open/closed/half-open)
        - Connection pool statistics
        - Last successful connection timestamp
        - Failed connection attempts count
        - Database connectivity test
        
        Returns:
            Dict with health check results
        """
        health_status = {
            "status": "unknown",
            "circuit_breaker": {
                "state": str(self.db_breaker.current_state),
                "failure_count": self.db_breaker.fail_counter,
                "fail_max": self.db_breaker.fail_max,
            },
            "connection_pool": {
                "size": self.pool_size,
                "total_connections_acquired": self.total_connections_acquired,
            },
            "last_successful_connection": self.last_successful_connection.isoformat() if self.last_successful_connection else None,
            "failed_connection_attempts": self.failed_connection_attempts,
            "connectivity_test": "not_tested"
        }
        
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT 1 as health_check")
                result = cursor.fetchone()
                cursor.close()
                
                if result and result[0] == 1:
                    health_status["status"] = "healthy"
                    health_status["connectivity_test"] = "passed"
                else:
                    health_status["status"] = "degraded"
                    health_status["connectivity_test"] = "unexpected_result"
                    
        except CircuitBreakerError:
            health_status["status"] = "circuit_breaker_open"
            health_status["connectivity_test"] = "circuit_breaker_blocking"
            logger.warning("Health check failed: circuit breaker is open")
        except ConnectionError as e:
            health_status["status"] = "unhealthy"
            health_status["connectivity_test"] = "failed"
            health_status["error"] = str(e)
            logger.error(f"Health check failed: {e}")
        except Exception as e:
            health_status["status"] = "unhealthy"
            health_status["connectivity_test"] = "failed"
            health_status["error"] = str(e)
            logger.error(f"Health check failed with unexpected error: {e}")
        
        return health_status
    
    def shutdown(self) -> None:
        """
        Gracefully shutdown the database connection pool.
        
        Closes all connections in the pool and waits for active queries to complete.
        Should be called during application shutdown.
        """
        if not self.pool:
            logger.warning("Database pool already closed or not initialized")
            return
        
        try:
            logger.info("Closing database connection pool...")
            
            self.pool.closeall()
            
            logger.info(
                f"Database connection pool closed successfully. "
                f"Total connections acquired during lifetime: {self.total_connections_acquired}"
            )
            
        except Exception as e:
            logger.error(f"Error closing database connection pool: {e}")
            raise
