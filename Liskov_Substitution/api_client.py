"""API Client for communicating with the backend application.

This module provides a clean, well-structured client for making
HTTP requests to the backend API with proper error handling.
"""
import re
from typing import Dict, Optional, List
import httpx
from src.config.settings import get_config
from src.models.api_types import APIErrorType
from src.utils.logger import get_logger

logger = get_logger(__name__)

class APIClientError(Exception):
    """Custom exception for API client errors."""
    
    def __init__(self, error_type: APIErrorType, message: str, status_code: int = None):
        self.error_type = error_type
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)
    
    def to_dict(self) -> Dict:
        """Convert exception to dictionary response."""
        return {
            "success": False,
            "error_type": self.error_type.value,
            "message": self.message
        }

class APIClient:
    """Client for interacting with the backend API.
    
    Provides methods for starting calls, sending emails, and managing
    Calendly invites with comprehensive error handling.
    """
    
    PHONE_MIN_LENGTH = 7
    PHONE_MAX_LENGTH = 15
    DEFAULT_TIMEOUT = 30.0
    HEALTH_CHECK_TIMEOUT = 5.0
    MAX_ERROR_MESSAGE_LENGTH = 200
    
    def __init__(self):
        """Initialize the API client with configuration."""
        self._config = get_config()
        self._base_url = self._config.api_base_url
        self._timeout = self.DEFAULT_TIMEOUT
        self._headers = {"X-API-Key": self._config.x_api_key}
    
    def _validate_phone_number(self, phone_number: str) -> tuple[bool, str]:
        """Validate phone number format.
        
        Args:
            phone_number: The phone number to validate
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        if not phone_number:
            return False, "Phone number is empty"
        
        cleaned = re.sub(r'[\s\-()\+]', '', phone_number)
        
        if not cleaned:
            return False, "Phone number is empty after cleaning"
        
        if not cleaned.isdigit():
            return False, "Phone number contains non-numeric characters"
        
        if len(cleaned) < self.PHONE_MIN_LENGTH or len(cleaned) > self.PHONE_MAX_LENGTH:
            return False, f"Phone number length invalid (must be {self.PHONE_MIN_LENGTH}-{self.PHONE_MAX_LENGTH} digits, got {len(cleaned)})"
        
        return True, ""
    
    def _validate_email(self, email: str) -> tuple[bool, str]:
        """Validate email format.
        
        Args:
            email: The email to validate
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        if not email or not isinstance(email, str):
            return False, "Email is required"
        
        email_pattern = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
        if not email_pattern.match(email.strip()):
            return False, "Invalid email format"
        
        return True, ""
    
    def _parse_http_error(self, error: httpx.HTTPStatusError, context: str) -> APIClientError:
        """Parse HTTP error response into APIClientError.
        
        Args:
            error: The HTTP status error
            context: Context string for logging
            
        Returns:
            Configured APIClientError
        """
        status_code = error.response.status_code
        error_type = APIErrorType.API_ERROR
        message = f"API returned error: {status_code}"
        
        try:
            response_json = error.response.json()
            detail = response_json.get("detail", "")
            
            if detail:
                detail_lower = detail.lower()
                
                if "not authorized to call" in detail_lower or "international permissions" in detail_lower or "21215" in detail:
                    error_type = APIErrorType.PERMISSION_DENIED
                    message = "Account not authorized to call this number. International permissions may be required."
                elif "not allowed to call" in detail_lower or "21216" in detail:
                    error_type = APIErrorType.INVALID_NUMBER
                    message = "Account not allowed to call this number"
                elif "is not valid" in detail_lower:
                    error_type = APIErrorType.INVALID_NUMBER
                    match = re.search(r'The phone number .+? is not valid\.', detail, re.IGNORECASE)
                    message = match.group(0) if match else "Invalid phone number format"
                elif "unable to create record" in detail_lower:
                    parts = detail.split("Unable to create record:")
                    message = parts[1].split("\n")[0].strip() if len(parts) > 1 else "Unable to create call record"
                else:
                    message = detail[:self.MAX_ERROR_MESSAGE_LENGTH]
        except Exception as parse_error:
            logger.warning(f"Failed to parse API error response for {context}: {parse_error}")
        
        logger.error(f"HTTP error in {context}: {status_code} - {message}")
        return APIClientError(error_type, message, status_code)
    
    def _make_request(
        self,
        method: str,
        endpoint: str,
        params: Dict = None,
        json_data: Dict = None,
        timeout: float = None
    ) -> Dict:
        """Make an HTTP request to the API.
        
        Args:
            method: HTTP method (GET, POST, etc.)
            endpoint: API endpoint path
            params: Query parameters
            json_data: JSON body data
            timeout: Request timeout
            
        Returns:
            Response JSON as dictionary
            
        Raises:
            APIClientError: If request fails
        """
        url = f"{self._base_url}/{endpoint.lstrip('/')}"
        request_timeout = timeout or self._timeout
        
        try:
            with httpx.Client(timeout=request_timeout, verify=False) as client:
                response = client.request(
                    method=method,
                    url=url,
                    params=params,
                    json=json_data,
                    headers=self._headers
                )
                response.raise_for_status()
                return response.json()
                
        except httpx.HTTPStatusError as e:
            raise self._parse_http_error(e, f"{method} {endpoint}")
            
        except httpx.TimeoutException as e:
            logger.error(f"Timeout error calling {endpoint}: {e}")
            raise APIClientError(
                APIErrorType.TIMEOUT_ERROR,
                f"Request timed out after {request_timeout}s"
            )
            
        except httpx.RequestError as e:
            logger.error(f"Request error calling {endpoint}: {e}")
            raise APIClientError(
                APIErrorType.NETWORK_ERROR,
                f"Failed to connect to API: {str(e)}"
            )
    
    def start_call(self, phone_number: str) -> Dict:
        """Start a call to the specified phone number.
        
        Args:
            phone_number: The phone number to call
            
        Returns:
            Dictionary with success status and call SID or error details
        """
        is_valid, validation_error = self._validate_phone_number(phone_number)
        if not is_valid:
            return {
                "success": False,
                "error_type": APIErrorType.INVALID_NUMBER.value,
                "message": validation_error
            }
        
        try:
            result = self._make_request(
                method="POST",
                endpoint="/start-call",
                params={"call_to_number": phone_number}
            )
            logger.info(f"API response for start_call: {result}")
            call_sid = result.get("call_sid") or result.get("callSid")
            return {"success": True, "callSid": call_sid}
            
        except APIClientError as e:
            return e.to_dict()
        except Exception as e:
            logger.exception(f"Unexpected error in start_call: {e}")
            return {
                "success": False,
                "error_type": APIErrorType.API_ERROR.value,
                "message": str(e)
            }
    
    def health_check(self) -> bool:
        """Check if the API is healthy and responding.
        
        Returns:
            True if API is healthy, False otherwise
        """
        try:
            url = f"{self._base_url}/health"
            with httpx.Client(timeout=self.HEALTH_CHECK_TIMEOUT) as client:
                response = client.get(url)
                return response.status_code == 200
        except Exception as e:
            logger.debug(f"Health check failed: {e}")
            return False
    
    def send_email(
        self,
        to_email: str,
        lead_id: str,
        email_sequence_number: str = "1"
    ) -> Dict:
        """Send email to lead via API.
        
        Args:
            to_email: Recipient email address
            lead_id: Lead identifier
            email_sequence_number: Email sequence number (default: "1")
            
        Returns:
            Dictionary with success status and response or error
        """
        is_valid, validation_error = self._validate_email(to_email)
        if not is_valid:
            return {"success": False, "error": validation_error}
        
        if not lead_id:
            return {"success": False, "error": "Lead ID is required"}
        
        try:
            result = self._make_request(
                method="POST",
                endpoint="/send-email",
                json_data={
                    "to_email": to_email,
                    "lead_id": lead_id,
                    "email_sequence_number": email_sequence_number
                }
            )
            return {"success": True, "response": result}
            
        except APIClientError as e:
            return {"success": False, "error": e.message}
        except Exception as e:
            logger.exception(f"Unexpected error in send_email: {e}")
            return {"success": False, "error": str(e)}
    
    def send_calendly_invite(
        self,
        email: str,
        time_slots: Optional[List] = None
    ) -> Dict:
        """Send Calendly invite via API.
        
        Args:
            email: Recipient email address
            time_slots: Optional list of time slots
            
        Returns:
            Dictionary with success status and response or error
        """
        is_valid, validation_error = self._validate_email(email)
        if not is_valid:
            return {"success": False, "error": validation_error}
        
        try:
            payload = {"email": email}
            if time_slots:
                payload["time_slots"] = time_slots
            
            result = self._make_request(
                method="POST",
                endpoint="/send-calendly-invite",
                json_data=payload
            )
            return {"success": True, "response": result}
            
        except APIClientError as e:
            return {"success": False, "error": e.message}
        except Exception as e:
            logger.exception(f"Unexpected error in send_calendly_invite: {e}")
            return {"success": False, "error": str(e)}

api_client = APIClient()
