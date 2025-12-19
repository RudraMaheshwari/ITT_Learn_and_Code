"""Input validators for repository operations.

This module provides reusable validation functions with security
considerations for sanitizing and validating user inputs.
"""
import re
from typing import Optional
from src.config.settings import get_config
from src.database.exceptions import ValidationError

CALL_SID_PATTERN = re.compile(r'^CA[a-f0-9]{32}$', re.IGNORECASE)

EMAIL_PATTERN = re.compile(
    r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
)

UUID_PATTERN = re.compile(
    r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$',
    re.IGNORECASE
)

def _get_pagination_config():
    """Get pagination configuration from settings."""
    config = get_config()
    return (
        config.pagination_max_page_size,
        config.pagination_min_page,
        config.pagination_default_page_size
    )

def validate_call_sid(call_sid: Optional[str], field_name: str = "call_sid") -> str:
    """Validate Twilio call SID format.
    
    Args:
        call_sid: The call SID to validate
        field_name: Name of the field for error messages
        
    Returns:
        Validated and stripped call SID
        
    Raises:
        ValidationError: If call_sid is invalid
    """
    if not call_sid:
        raise ValidationError(field_name, "cannot be empty")
    
    if not isinstance(call_sid, str):
        raise ValidationError(field_name, "must be a string")
    
    cleaned = call_sid.strip()
    
    if not cleaned:
        raise ValidationError(field_name, "cannot be empty or whitespace only")
    
    if not CALL_SID_PATTERN.match(cleaned):
        raise ValidationError(field_name, "invalid Twilio call SID format")
    
    return cleaned

def validate_call_sid_loose(call_sid: Optional[str], field_name: str = "call_sid") -> Optional[str]:
    """Validate call SID with loose validation (allows any non-empty string).
    
    Used for backward compatibility where strict Twilio format isn't enforced.
    
    Args:
        call_sid: The call SID to validate
        field_name: Name of the field for error messages
        
    Returns:
        Validated and stripped call SID, or None if invalid
    """
    if not call_sid or not isinstance(call_sid, str):
        return None
    
    cleaned = call_sid.strip()
    return cleaned if cleaned else None

def validate_email(email: Optional[str], field_name: str = "email") -> str:
    """Validate email format.
    
    Args:
        email: The email to validate
        field_name: Name of the field for error messages
        
    Returns:
        Validated and lowercased email
        
    Raises:
        ValidationError: If email is invalid
    """
    if not email:
        raise ValidationError(field_name, "cannot be empty")
    
    if not isinstance(email, str):
        raise ValidationError(field_name, "must be a string")
    
    cleaned = email.strip().lower()
    
    if not cleaned:
        raise ValidationError(field_name, "cannot be empty or whitespace only")
    
    if len(cleaned) > 254:
        raise ValidationError(field_name, "exceeds maximum length of 254 characters")
    
    if not EMAIL_PATTERN.match(cleaned):
        raise ValidationError(field_name, "invalid email format")
    
    return cleaned

def validate_uuid(value: Optional[str], field_name: str = "id") -> str:
    """Validate UUID format.
    
    Args:
        value: The UUID to validate
        field_name: Name of the field for error messages
        
    Returns:
        Validated UUID string
        
    Raises:
        ValidationError: If UUID is invalid
    """
    if not value:
        raise ValidationError(field_name, "cannot be empty")
    
    if not isinstance(value, str):
        raise ValidationError(field_name, "must be a string")
    
    cleaned = value.strip().lower()
    
    if not UUID_PATTERN.match(cleaned):
        raise ValidationError(field_name, "invalid UUID format")
    
    return cleaned

def validate_pagination(
    page: int = 1,
    per_page: int = None
) -> tuple[int, int, int]:
    """Validate pagination parameters.
    
    Args:
        page: Page number (1-indexed)
        per_page: Number of items per page
        
    Returns:
        Tuple of (validated_page, validated_per_page, offset)
        
    Raises:
        ValidationError: If pagination parameters are invalid
    """
    max_page_size, min_page, default_page_size = _get_pagination_config()
    
    if per_page is None:
        per_page = default_page_size
    
    if not isinstance(page, int) or page < min_page:
        page = min_page
    
    if not isinstance(per_page, int) or per_page < 1:
        per_page = default_page_size
    elif per_page > max_page_size:
        per_page = max_page_size
    
    offset = (page - 1) * per_page
    
    return page, per_page, offset

def sanitize_string(
    value: Optional[str],
    max_length: int = 500,
    field_name: str = "value"
) -> Optional[str]:
    """Sanitize string input for safe database storage.
    
    Args:
        value: The string to sanitize
        max_length: Maximum allowed length
        field_name: Name of the field for error messages
        
    Returns:
        Sanitized string or None if empty
    """
    if value is None:
        return None
    
    if not isinstance(value, str):
        return None
    
    cleaned = value.strip()
    
    if not cleaned:
        return None
    
    if len(cleaned) > max_length:
        cleaned = cleaned[:max_length]
    
    dangerous_patterns = ['<script', 'javascript:', 'on\w+\s*=']
    for pattern in dangerous_patterns:
        cleaned = re.sub(pattern, '', cleaned, flags=re.IGNORECASE)
    
    return cleaned

def sanitize_phone_number(phone: Optional[str]) -> Optional[str]:
    """Sanitize and validate phone number.
    
    Args:
        phone: The phone number to sanitize
        
    Returns:
        Sanitized phone number or None if invalid
    """
    if not phone or not isinstance(phone, str):
        return None
    
    digits_only = re.sub(r'[^\d+]', '', phone.strip())
    
    if len(digits_only) < 10:
        return None
    
    return digits_only[:20]
