"""
Call Session Service - Business logic layer for call session management.
Handles session initialization, status tracking, and conversation persistence.
"""
import uuid
from typing import Dict, List, Tuple
from src.services.transcript_extractor import TranscriptExtractor
from src.database.postgres_repository import PostgreSQLSessionRepository
from src.config.settings import get_config
from src.api.utils import sanitize_call_sid
from src.utils.logger import logger


class CallSessionService:
    """Service layer for managing call sessions and transcripts."""
    
    def __init__(self, session_repo: PostgreSQLSessionRepository = None):
        """
        Initialize the call session service.
        
        Args:
            session_repo: Optional repository instance (creates new if not provided)
        """
        config = get_config()
        
        if session_repo:
            self.session_repo = session_repo
        else:
            pg_config = config.get_postgres_connection_dict()
            if not pg_config:
                raise ConnectionError(
                    "PostgreSQL configuration is required for CallSessionService but missing. "
                    "Please set POSTGRES_DATABASE, POSTGRES_USER, and POSTGRES_PASSWORD environment variables."
                )
            
            resilience_config = config.get_postgres_resilience_config()
            
            try:
                self.session_repo = PostgreSQLSessionRepository(
                    connection_config=pg_config,
                    pool_size=resilience_config['pool_size'],
                    max_retry_attempts=resilience_config['max_retry_attempts'],
                    circuit_breaker_fail_max=resilience_config['circuit_breaker_fail_max'],
                    circuit_breaker_timeout=resilience_config['circuit_breaker_timeout']
                )
                logger.info(
                    f"Call session service initialized with PostgreSQL "
                    f"(pool={resilience_config['pool_size']}, "
                    f"retry={resilience_config['max_retry_attempts']}, "
                    f"circuit_breaker_max={resilience_config['circuit_breaker_fail_max']})"
                )
            except Exception as e:
                logger.error(f"Failed to initialize PostgreSQL session repository: {e}")
                raise ConnectionError(
                    f"PostgreSQL connection failed for CallSessionService. This is required. "
                    f"Error: {e}"
                ) from e
    
    def initialize_call(self, call_sid: str, phone_number: str = None) -> Tuple[str, str]:
        """
        Initialize a new call session in the database.
        
        Args:
            call_sid: Twilio call identifier
            phone_number: Optional phone number being called
            
        Returns:
            Tuple of (call_sid as user_id, generated thread_id)
            
        Raises:
            Exception: If session creation fails
        """
        if not self.session_repo:
            raise RuntimeError("Session repository not available - PostgreSQL connection required")
        
        thread_id = str(uuid.uuid4())
        
        success = self.session_repo.create_session(call_sid, thread_id, phone_number)
        
        if success:
            sanitized_sid = sanitize_call_sid(call_sid)
            logger.info(f"Initialized call {sanitized_sid}")
            return call_sid, thread_id
        else:
            sanitized_sid = sanitize_call_sid(call_sid)
            logger.error(f"Failed to initialize call session {sanitized_sid} in database, using local thread_id")
            return call_sid, thread_id
    
    def update_call_status(self, call_sid: str, status: str) -> bool:
        """
        Update call status (handles all status transitions).
        
        Args:
            call_sid: Twilio call identifier
            status: Call status from Twilio
            
        Returns:
            True if successful, False otherwise
        """
        if not self.session_repo:
            raise RuntimeError("Session repository not available - PostgreSQL connection required")
        
        valid_statuses = [
            'initiated', 'ringing', 'answered', 'in-progress',
            'completed', 'failed', 'busy', 'no-answer', 'canceled'
        ]
        
        normalized_status = status.lower().replace(' ', '-')
        
        if normalized_status not in valid_statuses:
            logger.warning(f"Invalid status: {status}, normalizing to 'failed'")
            normalized_status = 'failed'
        
        return self.session_repo.update_session_status(call_sid, normalized_status)
    
    def update_call_metadata(self, call_sid: str, duration_seconds: int = None, 
                            phone_number: str = None) -> bool:
        """
        Update call metadata (duration, phone number).
        
        Args:
            call_sid: Twilio call identifier
            duration_seconds: Call duration from Twilio
            phone_number: Phone number if not already set
            
        Returns:
            True if successful, False otherwise
        """
        if not self.session_repo:
            raise RuntimeError("Session repository not available - PostgreSQL connection required")
        
        return self.session_repo.update_session_metadata(
            call_sid, duration_seconds, phone_number
        )
    
    def save_conversation(self, call_sid: str, messages: List[Dict], 
                         final_status: str = 'completed',
                         usage_metrics: dict = None) -> bool:
        """
        Save complete conversation transcript and extract state from transcript.
        
        Args:
            call_sid: Twilio call identifier
            messages: List of message dictionaries with role/content
            final_status: Final call status ('completed', 'failed', etc.)
            usage_metrics: Optional dictionary with token usage metrics
            
        Returns:
            True if successful, False otherwise
        """
        if not self.session_repo:
            raise RuntimeError("Session repository not available - PostgreSQL connection required")
        
        try:
            if final_status == 'completed' and len(messages) < 2:
                final_status = 'failed'
            
            success = self.session_repo.save_transcript(call_sid, messages, final_status)
            
            if success:
                sanitized_sid = sanitize_call_sid(call_sid)
                logger.info(f"Saved conversation for call {sanitized_sid} with status: {final_status}")
                
                if usage_metrics:
                    try:
                        self.session_repo.save_usage_metrics(call_sid, usage_metrics)
                        logger.info(f"Saved usage metrics for call {sanitized_sid}")
                        logger.debug(f"Usage metrics: {usage_metrics}")
                    except Exception as e:
                        logger.error("Error saving usage metrics")
                        logger.debug(f"Usage metrics error: {e}")
                
                try:
                    logger.info(f"Starting transcript extraction for call {sanitized_sid}")
                    extractor = TranscriptExtractor()
                    extracted_data = extractor.extract_conversation_state(messages)
                    logger.info(f"Transcript extraction completed for call {sanitized_sid}: {bool(extracted_data)}")
                    
                    if extracted_data:
                        logger.info(f"[EXTRACT][{sanitized_sid}] Extracted data: business_intent={extracted_data.get('business_intent')}, purchase_intent={extracted_data.get('purchase_intent')}, email={extracted_data.get('email')}, reschedule={extracted_data.get('reschedule')}")
                        if extracted_data.get('conversation_summary'):
                            logger.info(f"[EXTRACT][{sanitized_sid}] Summary: {extracted_data.get('conversation_summary')}")
                        
                        try:
                            self.session_repo.save_conversation_state(call_sid, extracted_data)
                            logger.info(f"[EXTRACT][{sanitized_sid}] Successfully saved conversation state to database")
                        except Exception as e:
                            logger.error(f"[EXTRACT][{sanitized_sid}] Error saving conversation state: {e}")
                    else:
                        logger.warning(f"[EXTRACT][{sanitized_sid}] No data extracted from transcript")
                    
                except Exception as e:
                    logger.error("Error extracting conversation data from transcript")
                    logger.debug(f"Extraction error: {e}")
                
                return True
            else:
                sanitized_sid = sanitize_call_sid(call_sid)
                logger.error(f"Failed to save conversation for call {sanitized_sid}")
                return False
        except Exception as e:
            logger.exception("Error saving conversation")
            logger.debug(f"Conversation save error: {e}")
            return False
    
    def update_answered_status(self, call_sid: str, answered_status: str) -> bool:
        """
        Update answered status from AMD (Answering Machine Detection) callback.
        
        Args:
            call_sid: Twilio call identifier
            answered_status: Status value ('voicemail', 'human', 'unknown')
            
        Returns:
            True if successful, False otherwise
            
        Raises:
            ValueError: If answered_status is not a valid value
        """
        if not self.session_repo:
            raise RuntimeError("Session repository not available - PostgreSQL connection required")
        
        valid_statuses = ['voicemail', 'human', 'unknown']
        
        normalized_status = answered_status.lower().strip()
        
        if normalized_status not in valid_statuses:
            logger.warning(f"Invalid answered_status: {answered_status}, must be one of {valid_statuses}")
            return False
        
        return self.session_repo.update_answered_status(call_sid, normalized_status)


