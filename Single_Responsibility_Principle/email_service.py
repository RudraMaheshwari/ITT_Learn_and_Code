import json
import re
import requests
from typing import List, Dict, Optional
from src.config.settings import get_config
from src.utils.logger import get_logger

logger = get_logger(__name__)

class EmailService:
    """
    Service to send emails via Logic App.
    Supports TEST MODE for development and PRODUCTION mode for Logic App integration.
    """

    def __init__(self):
        self.config = get_config()
        self.logic_app_url = getattr(self.config, 'logic_app_webhook_url', None)
        self.test_mode = getattr(self.config, 'logic_app_test_mode', True)
        self.timeout = self.config.logic_app_timeout_seconds
        
        self.email_pattern = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
    
    def _is_valid_email(self, email: str) -> bool:
        """Validate email format using regex."""
        return bool(self.email_pattern.match(email.strip()))

    def send_emails_to_leads(self, emails: List[str], names: List[str]) -> Dict:
        """
        Send emails to leads via Logic App.
        
        Args:
            emails: List of email addresses
            names: List of names (matched by index with emails)
            
        Returns:
            Dict with status and message:
            {
                "success": True/False,
                "message": "Success message or error",
                "payload": {...},
                "response": {...}
            }
        """
        
        if not emails or not names:
            return {
                "success": False,
                "message": "No emails or names provided",
                "payload": None
            }
        
        if len(emails) != len(names):
            return {
                "success": False,
                "message": f"Mismatch: {len(emails)} emails but {len(names)} names",
                "payload": None
            }
        
        invalid_emails = [email for email in emails if not self._is_valid_email(email)]
        if invalid_emails:
            logger.warning(f"Invalid email addresses provided: {invalid_emails}")
            return {
                "success": False,
                "message": f"Invalid email format: {', '.join(invalid_emails)}",
                "payload": None
            }
        
        payload = {
            "emails": emails,
            "names": names
        }
        
        logger.info(f"Preparing to send emails to {len(emails)} leads")
        logger.debug(f"Payload: {json.dumps(payload, indent=2)}")
        
        if self.test_mode:
            logger.info("🧪 TEST MODE: Email sending simulation")
            logger.info(f"📧 Would send to {len(emails)} recipients:")
            for i, (email, name) in enumerate(zip(emails, names), 1):
                logger.info(f"  {i}. {name} <{email}>")
            
            return {
                "success": True,
                "message": f"✅ TEST MODE: Payload validated. Ready to send to {len(emails)} leads.",
                "payload": payload,
                "test_mode": True
            }
        
        if not self.logic_app_url:
            return {
                "success": False,
                "message": "❌ Logic App webhook URL not configured. Set LOGIC_APP_WEBHOOK_URL in .env",
                "payload": payload
            }
        
        try:
            logger.info(f"📤 Calling Logic App: {self.logic_app_url}")
            
            response = requests.post(
                self.logic_app_url,
                json=payload,
                headers={
                    "Content-Type": "application/json"
                },
                timeout=self.timeout
            )
            
            if response.status_code == 200 or response.status_code == 202:
                logger.info(f"✅ Logic App responded with status {response.status_code}")
                
                try:
                    response_data = response.json()
                except Exception:
                    response_data = {"raw_response": response.text}
                
                return {
                    "success": True,
                    "message": f"✅ Sending to {len(emails)} leads",
                    "payload": payload,
                    "response": response_data,
                    "status_code": response.status_code
                }
            else:
                logger.error(f"❌ Logic App returned error status {response.status_code}")
                logger.error(f"Response: {response.text}")
                
                return {
                    "success": False,
                    "message": f"❌ Logic App error: HTTP {response.status_code}",
                    "payload": payload,
                    "response": response.text,
                    "status_code": response.status_code
                }
        
        except requests.exceptions.Timeout:
            logger.error(f"⏱️ Timeout calling Logic App after {self.timeout}s")
            return {
                "success": False,
                "message": f"⏱️ Request timeout after {self.timeout} seconds",
                "payload": payload
            }
        
        except requests.exceptions.ConnectionError as e:
            logger.error(f"🔌 Connection error to Logic App: {e}")
            return {
                "success": False,
                "message": "🔌 Cannot connect to Logic App. Check URL and network.",
                "payload": payload
            }
        
        except Exception as e:
            logger.exception(f"❌ Unexpected error calling Logic App: {e}")
            return {
                "success": False,
                "message": f"❌ Error: {str(e)}",
                "payload": payload
            }

_email_service = None

def get_email_service() -> EmailService:
    """Get or create EmailService singleton instance"""
    global _email_service
    if _email_service is None:
        _email_service = EmailService()
    return _email_service