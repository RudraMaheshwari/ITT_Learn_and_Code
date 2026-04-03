from datetime import datetime
from typing import Optional
from src.database.base_repository import BaseRepository
from src.utils.logger import logger

class LeadTrackingRepository:
    """Repository for lead_tracking table operations."""
    
    def __init__(self, base_repo: BaseRepository):
        """
        Initialize the lead tracking repository.
        
        Args:
            base_repo: Base repository for database connections
        """
        self.base_repo = base_repo
    
    def _init_table(self):
        """Initialize lead_tracking table."""
        try:
            with self.base_repo._get_connection() as conn:
                cursor = conn.cursor()
                
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS lead_tracking (
                        lead_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                        call_sid VARCHAR NOT NULL,
                        name VARCHAR,
                        email VARCHAR UNIQUE,
                        contact_number VARCHAR,
                        status VARCHAR DEFAULT 'new' CHECK (status IN ('new', 'active', 'client_signed', 'archive')),
                        form_submitted BOOLEAN DEFAULT FALSE,
                        payment_done BOOLEAN DEFAULT FALSE,
                        email_sent BOOLEAN DEFAULT FALSE,
                        created_at TIMESTAMP DEFAULT NOW()
                    )
                """)
                
                cursor.execute("""
                    CREATE INDEX IF NOT EXISTS idx_lead_tracking_call_sid 
                    ON lead_tracking(call_sid)
                """)
                
                cursor.execute("""
                    CREATE INDEX IF NOT EXISTS idx_lead_tracking_email 
                    ON lead_tracking(email)
                """)
                
                cursor.execute("""
                    CREATE INDEX IF NOT EXISTS idx_lead_tracking_status 
                    ON lead_tracking(status)
                """)
                
                conn.commit()
                logger.info("Lead tracking table initialized successfully")
        except Exception as e:
            logger.error(f"Error initializing lead_tracking table: {e}")
            raise

    def update_lead_tracking(self, lead_id: str, **kwargs) -> bool:
        """Update the lead tracking for a lead."""
        try:
            with self.base_repo._get_connection() as conn:
                cursor = conn.cursor()
                set_clause = ', '.join([f'{key} = %s' for key in kwargs.keys()])
                values = list(kwargs.values()) + [lead_id]
                
                query = f"""
                    UPDATE lead_tracking
                    SET {set_clause}
                    WHERE lead_id = %s
                """
                cursor.execute(query, values)
                conn.commit()
                logger.info(f"Updated lead {lead_id}: {kwargs}")
                return True
        except Exception as e:
            logger.error(f"Error updating lead tracking for {lead_id}: {e}")
            return False

    def check_payment_status(self, lead_id: str) -> bool:
        """Check if payment has been completed for a lead."""
        try:
            with self.base_repo._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT payment_done FROM lead_tracking WHERE lead_id = %s", (lead_id,))
                result = cursor.fetchone()
                return result[0] if result else False
        except Exception as e:
            logger.error(f"Error checking payment status for {lead_id}: {e}")
            return False

    def check_form_submitted(self, lead_id: str) -> bool:
        """Check if form has been submitted by a lead."""
        try:
            with self.base_repo._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT form_submitted FROM lead_tracking WHERE lead_id = %s", (lead_id,))
                result = cursor.fetchone()
                return result[0] if result else False
        except Exception as e:
            logger.error(f"Error checking form submission for {lead_id}: {e}")
            return False

    def update_status(self, lead_id: str, status: str) -> bool:
        """Update the status of a lead."""
        try:
            with self.base_repo._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    UPDATE lead_tracking
                    SET status = %s
                    WHERE lead_id = %s
                """, (status, lead_id))
                conn.commit()
                logger.info(f"Updated lead {lead_id} status to {status}")
                return True
        except Exception as e:
            logger.error(f"Error updating status for {lead_id}: {e}")
            return False

    def get_lead_by_id(self, lead_id: str) -> Optional[dict]:
        """Get lead by ID."""
        try:
            with self.base_repo._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT lead_id, call_sid, name, email, contact_number, 
                           status, form_submitted, payment_done, email_sent, created_at
                    FROM lead_tracking
                    WHERE lead_id = %s
                """, (lead_id,))
                result = cursor.fetchone()
                if result:
                    return {
                        'lead_id': str(result[0]),
                        'call_sid': result[1],
                        'name': result[2],
                        'email': result[3],
                        'contact_number': result[4],
                        'status': result[5],
                        'form_submitted': result[6],
                        'payment_done': result[7],
                        'email_sent': result[8],
                        'created_at': result[9]
                    }
                return None
        except Exception as e:
            logger.error(f"Error getting lead {lead_id}: {e}")
            return None

    def get_lead_by_email(self, email: str) -> Optional[dict]:
        """Get lead by email address."""
        try:
            with self.base_repo._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT lead_id, call_sid, name, email, contact_number, 
                           status, form_submitted, payment_done, email_sent, created_at
                    FROM lead_tracking
                    WHERE email = %s
                """, (email,))
                result = cursor.fetchone()
                if result:
                    return {
                        'lead_id': str(result[0]),
                        'call_sid': result[1],
                        'name': result[2],
                        'email': result[3],
                        'contact_number': result[4],
                        'status': result[5],
                        'form_submitted': result[6],
                        'payment_done': result[7],
                        'email_sent': result[8],
                        'created_at': result[9]
                    }
                return None
        except Exception as e:
            logger.error(f"Error getting lead by email {email}: {e}")
            return None
