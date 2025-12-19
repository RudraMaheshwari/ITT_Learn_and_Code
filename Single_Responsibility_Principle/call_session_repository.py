import json
from datetime import datetime
from typing import Dict, List, Optional
from src.database.base_repository import BaseRepository
from src.api.utils import sanitize_call_sid
from src.utils.logger import logger

class CallSessionRepository:
    """Repository for call_sessions table operations."""
    
    def __init__(self, base_repo: BaseRepository):
        """
        Initialize the call session repository.
        
        Args:
            base_repo: Base repository for database connections
        """
        self.base_repo = base_repo
    
    def _init_table(self):
        """Initialize call_sessions table and indexes."""
        try:
            with self.base_repo._get_connection() as conn:
                cursor = conn.cursor()
                
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS call_sessions (
                        call_sid TEXT PRIMARY KEY,
                        thread_id TEXT NOT NULL,
                        user_id TEXT NOT NULL,
                        phone_number TEXT,
                        status TEXT NOT NULL,
                        transcript_data JSONB,
                        message_count INTEGER DEFAULT 0,
                        duration_seconds INTEGER,
                        start_time TIMESTAMP,
                        end_time TIMESTAMP,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """)
                
                cursor.execute("""
                    CREATE INDEX IF NOT EXISTS idx_call_sessions_status 
                    ON call_sessions(status)
                """)
                
                cursor.execute("""
                    CREATE INDEX IF NOT EXISTS idx_call_sessions_user_id 
                    ON call_sessions(user_id)
                """)
                
                cursor.execute("""
                    CREATE INDEX IF NOT EXISTS idx_call_sessions_created_at 
                    ON call_sessions(created_at DESC)
                """)               
                cursor.execute("""
                    SELECT column_name 
                    FROM information_schema.columns 
                    WHERE table_name = 'call_sessions' AND column_name = 'answered_status'
                """)
                has_answered_status = cursor.fetchone() is not None
                
                if not has_answered_status:
                    logger.info("Adding answered_status column to call_sessions table")
                    cursor.execute("""
                        ALTER TABLE call_sessions 
                        ADD COLUMN answered_status TEXT
                    """)
                    cursor.execute("""
                        CREATE INDEX IF NOT EXISTS idx_call_sessions_answered_status 
                        ON call_sessions(answered_status)
                    """)
                
                conn.commit()
                logger.info("Call sessions table initialized successfully")
        except Exception as e:
            logger.error(f"Error initializing call_sessions table: {e}")
            raise
    
    def create_session(self, call_sid: str, thread_id: str, phone_number: str = None) -> bool:
        """
        Create a new call session in the database.
        
        Args:
            call_sid: Twilio call identifier
            thread_id: Unique thread identifier for LangGraph
            phone_number: Optional phone number being called
            
        Returns:
            True if successful, False otherwise
        """
        try:
            with self.base_repo._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO call_sessions 
                    (call_sid, thread_id, user_id, phone_number, status, start_time)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """, (call_sid, thread_id, call_sid, phone_number, 'initiated', datetime.utcnow()))
                conn.commit()
                sanitized_sid = sanitize_call_sid(call_sid)
                logger.info(f"Created session for call {sanitized_sid}")
                return True
        except Exception as e:
            sanitized_sid = sanitize_call_sid(call_sid) if call_sid else "***"
            logger.error(f"Error creating session for {sanitized_sid}")
            logger.debug(f"Session creation error: {e}")
            return False
    
    def update_session_status(self, call_sid: str, status: str) -> bool:
        """
        Update session status with proper timestamps.
        
        Args:
            call_sid: Twilio call identifier
            status: New status ('initiated', 'ringing', 'answered', 'in-progress',
                               'completed', 'failed', 'busy', 'no-answer', 'canceled')
            
        Returns:
            True if successful, False otherwise
        """
        try:
            with self.base_repo._get_connection() as conn:
                cursor = conn.cursor()
                
                if status in ['answered', 'in-progress'] and self._session_exists(call_sid):
                    cursor.execute("""
                        UPDATE call_sessions 
                        SET status = %s, updated_at = %s
                        WHERE call_sid = %s AND start_time IS NULL
                    """, (status, datetime.utcnow(), call_sid))
                
                if status in ['completed', 'failed', 'busy', 'no-answer', 'canceled']:
                    cursor.execute("""
                        UPDATE call_sessions 
                        SET status = %s, end_time = %s, updated_at = %s
                        WHERE call_sid = %s
                    """, (status, datetime.utcnow(), datetime.utcnow(), call_sid))
                else:
                    cursor.execute("""
                        UPDATE call_sessions 
                        SET status = %s, updated_at = %s
                        WHERE call_sid = %s
                    """, (status, datetime.utcnow(), call_sid))
                
                conn.commit()
                sanitized_sid = sanitize_call_sid(call_sid)
                logger.debug(f"Updated session {sanitized_sid} status to {status}")
                return True
        except Exception as e:
                sanitized_sid = sanitize_call_sid(call_sid) if call_sid else "***"
                logger.error(f"Error updating session status for {sanitized_sid}")
                logger.debug(f"Status update error: {e}")
                return False
    
    def update_session_metadata(self, call_sid: str, duration_seconds: int = None,
                               phone_number: str = None) -> bool:
        """
        Update session metadata like duration and phone number.
        
        Args:
            call_sid: Twilio call identifier
            duration_seconds: Call duration in seconds
            phone_number: Phone number (fallback if not set)
            
        Returns:
            True if successful, False otherwise
        """
        try:
            with self.base_repo._get_connection() as conn:
                cursor = conn.cursor()
                
                updates = []
                params = []
                
                if duration_seconds is not None:
                    updates.append("duration_seconds = %s")
                    params.append(duration_seconds)
                
                if phone_number is not None:
                    updates.append("phone_number = COALESCE(phone_number, %s)")
                    params.append(phone_number)
                
                if updates:
                    updates.append("updated_at = %s")
                    params.append(datetime.utcnow())
                    params.append(call_sid)
                    
                    query = f"""
                        UPDATE call_sessions 
                        SET {', '.join(updates)}
                        WHERE call_sid = %s
                    """
                    cursor.execute(query, params)
                    conn.commit()
                    sanitized_sid = sanitize_call_sid(call_sid)
                    logger.debug(f"Updated metadata for {sanitized_sid}")
                    return True
                
                return True
        except Exception as e:
            sanitized_sid = sanitize_call_sid(call_sid) if call_sid else "***"
            logger.error(f"Error updating metadata for {sanitized_sid}")
            logger.debug(f"Metadata update error: {e}")
            return False
    
    def update_answered_status(self, call_sid: str, answered_status: str) -> bool:
        """
        Update answered status from AMD (Answering Machine Detection) callback.
        
        This method updates the answered_status column without modifying the status
        column (which contains Twilio's original status). This allows analytics to
        filter by voicemail vs human-answered calls while preserving Twilio's status.
        
        Args:
            call_sid: Twilio call identifier
            answered_status: Status value ('voicemail', 'human', 'unknown')
            
        Returns:
            True if successful, False otherwise
        """
        try:
            with self.base_repo._get_connection() as conn:
                cursor = conn.cursor()
                
                cursor.execute("""
                    UPDATE call_sessions 
                    SET answered_status = %s, updated_at = %s
                    WHERE call_sid = %s
                """, (answered_status, datetime.utcnow(), call_sid))
                
                conn.commit()
                
                if cursor.rowcount > 0:
                    sanitized_sid = sanitize_call_sid(call_sid)
                    logger.debug(f"Updated answered_status for {sanitized_sid} to {answered_status}")
                    return True
                else:
                    sanitized_sid = sanitize_call_sid(call_sid)
                    logger.warning(f"Session {sanitized_sid} not found when updating answered_status - will be set when session is created")
                    return False
                    
        except Exception as e:
            sanitized_sid = sanitize_call_sid(call_sid) if call_sid else "***"
            logger.error(f"Error updating answered_status for {sanitized_sid}")
            logger.debug(f"Answered status update error: {e}")
            return False
    
    def save_transcript(self, call_sid: str, messages: List[Dict], status: str = 'completed') -> bool:
        """
        Save complete transcript for a call.
        
        Args:
            call_sid: Twilio call identifier
            messages: List of message dictionaries with role/content
            status: Final call status
            
        Returns:
            True if successful, False otherwise
        """
        try:
            with self.base_repo._get_connection() as conn:
                cursor = conn.cursor()
                
                cursor.execute("""
                    UPDATE call_sessions
                    SET transcript_data = %s,
                        message_count = %s,
                        status = %s,
                        end_time = %s,
                        updated_at = %s
                    WHERE call_sid = %s
                """, (
                    json.dumps(messages),
                    len(messages),
                    status,
                    datetime.utcnow(),
                    datetime.utcnow(),
                    call_sid
                ))
                
                conn.commit()
                sanitized_sid = sanitize_call_sid(call_sid)
                logger.info(f"Saved transcript for call {sanitized_sid} with {len(messages)} messages")
                return True
        except Exception as e:
            sanitized_sid = sanitize_call_sid(call_sid) if call_sid else "***"
            logger.error(f"Error saving transcript for {sanitized_sid}")
            logger.debug(f"Transcript save error: {e}")
            return False
    
    def get_session(self, call_sid: str) -> Optional[Dict]:
        """
        Retrieve a session by call_sid.
        
        Args:
            call_sid: Twilio call identifier
            
        Returns:
            Session dictionary or None
        """
        try:
            with self.base_repo._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT call_sid, thread_id, user_id, phone_number, status, 
                           transcript_data, message_count, duration_seconds,
                           start_time, end_time, created_at, answered_status
                    FROM call_sessions
                    WHERE call_sid = %s
                """, (call_sid,))
                
                row = cursor.fetchone()
                if row:
                    return {
                        "call_sid": row[0],
                        "thread_id": row[1],
                        "user_id": row[2],
                        "phone_number": row[3],
                        "status": row[4],
                        "transcript_data": json.loads(row[5]) if row[5] else None,
                        "message_count": row[6],
                        "duration_seconds": row[7],
                        "start_time": row[8],
                        "end_time": row[9],
                        "created_at": row[10],
                        "answered_status": row[11]
                    }
                return None
        except Exception as e:
            sanitized_sid = sanitize_call_sid(call_sid) if call_sid else "***"
            logger.error(f"Error retrieving session for {sanitized_sid}")
            logger.debug(f"Session retrieval error: {e}")
            return None
    
    def _session_exists(self, call_sid: str) -> bool:
        """Check if session exists in database."""
        try:
            with self.base_repo._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT 1 FROM call_sessions WHERE call_sid = %s", (call_sid,))
                return cursor.fetchone() is not None
        except Exception as e:
            sanitized_sid = sanitize_call_sid(call_sid) if call_sid else "***"
            logger.error(f"Error checking session existence for {sanitized_sid}")
            logger.debug(f"Session existence check error: {e}")
            return False
