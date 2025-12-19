"""Repository for calendly_status table operations."""
from datetime import datetime
from typing import Optional, Dict, Any
from src.database.base_repository import BaseRepository
from src.utils.logger import logger

class CalendlyStatusRepository:
    """Repository for calendly_status table operations."""

    def __init__(self, base_repo: BaseRepository):
        self.base_repo = base_repo

    def create_table(self):
        """Create the calendly_status table if it doesn't exist."""
        create_sql = """
            CREATE TABLE IF NOT EXISTS calendly_status (
                id SERIAL PRIMARY KEY,
                lead_id UUID NOT NULL REFERENCES lead_tracking(lead_id),
                invite_sent BOOLEAN DEFAULT FALSE,
                invite_sent_at TIMESTAMP,
                booking_url TEXT
            )
        """
        try:
            with self.base_repo._get_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(create_sql)
                    conn.commit()
                    logger.info("calendly_status table created/verified")
                    return True
        except Exception as e:
            logger.error(f"Error creating calendly_status table: {e}")
            return False

    def create_calendly_invite(
        self,
        lead_id: str,
        booking_url: str
    ) -> bool:
        """Create a new Calendly invite record."""
        insert_sql = """
            INSERT INTO calendly_status (lead_id, invite_sent, invite_sent_at, booking_url)
            VALUES (%s, TRUE, %s, %s)
            RETURNING id
        """
        try:
            with self.base_repo._get_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(insert_sql, (lead_id, datetime.now(), booking_url))
                    result = cursor.fetchone()
                    conn.commit()
                    logger.info(f"Calendly invite created for lead_id: {lead_id}")
                    return True
        except Exception as e:
            logger.error(f"Error creating Calendly invite: {e}")
            return False

    def get_status_by_lead_id(self, lead_id: str) -> Optional[Dict[str, Any]]:
        """Get Calendly status by lead_id."""
        select_sql = """
            SELECT cs.id, cs.lead_id, cs.invite_sent, cs.invite_sent_at, cs.booking_url,
                   lt.email, lt.name
            FROM calendly_status cs
            JOIN lead_tracking lt ON cs.lead_id = lt.lead_id
            WHERE cs.lead_id = %s
            ORDER BY cs.invite_sent_at DESC
            LIMIT 1
        """
        try:
            with self.base_repo._get_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(select_sql, (lead_id,))
                    row = cursor.fetchone()
                    if row:
                        return {
                            'id': row[0],
                            'lead_id': str(row[1]),
                            'invite_sent': row[2],
                            'invite_sent_at': row[3],
                            'booking_url': row[4],
                            'email': row[5],
                            'name': row[6]
                        }
                    return None
        except Exception as e:
            logger.error(f"Error getting Calendly status: {e}")
            return None

    def get_status_by_email(self, email: str) -> Optional[Dict[str, Any]]:
        """Get Calendly status by email (via lead_tracking)."""
        select_sql = """
            SELECT cs.id, cs.lead_id, cs.invite_sent, cs.invite_sent_at, cs.booking_url,
                   lt.email, lt.name
            FROM calendly_status cs
            JOIN lead_tracking lt ON cs.lead_id = lt.lead_id
            WHERE lt.email = %s
            ORDER BY cs.invite_sent_at DESC
            LIMIT 1
        """
        try:
            with self.base_repo._get_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(select_sql, (email,))
                    row = cursor.fetchone()
                    if row:
                        return {
                            'id': row[0],
                            'lead_id': str(row[1]),
                            'invite_sent': row[2],
                            'invite_sent_at': row[3],
                            'booking_url': row[4],
                            'email': row[5],
                            'name': row[6]
                        }
                    return None
        except Exception as e:
            logger.error(f"Error getting Calendly status by email: {e}")
            return None
