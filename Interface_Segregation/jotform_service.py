import urllib.parse
import base64
from typing import Optional
from cryptography.fernet import Fernet
from src.config.settings import get_config
from src.utils.logger import logger

config = get_config()

class JotformService:
    def __init__(self, form_id: str | None = None, api_key: str | None = None):
        """
        Jotform service for generating dynamic form URLs and handling webhooks.
        Values can be injected or taken from settings.
        
        Args:
            form_id: Jotform form ID (can be from settings)
            api_key: Jotform API key (optional, for API operations)
        """
        self.form_id = form_id or config.jotform_form_id
        self.api_key = api_key or config.jotform_api_key
        self.base_url = config.jotform_base_url
        
        encryption_key = config.jotform_encryption_key
        if encryption_key:
            self._fernet = Fernet(encryption_key.encode())
        else:
            logger.warning(
                "JOTFORM_ENCRYPTION_KEY not set. Generate one using: "
                "python -c \"from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())\""
            )
            self._fernet = Fernet(Fernet.generate_key())
        
        if not self.form_id:
            raise ValueError("JOTFORM_FORM_ID is not set.")
        
        logger.info(f"JotformService initialized with form_id: {self.form_id}")

    def encrypt_lead_id(self, lead_id: str) -> str:
        """
        Encrypt the lead_id to create a secure, URL-safe token.
        
        This prevents exposing the actual lead_id in URLs while still
        allowing tracking through hidden form fields.
        
        Args:
            lead_id: The lead ID to encrypt
            
        Returns:
            URL-safe encrypted token
        """
        encrypted = self._fernet.encrypt(lead_id.encode())
        token = base64.urlsafe_b64encode(encrypted).decode()
        logger.debug(f"Encrypted lead_id to token (length: {len(token)})")
        return token

    def decrypt_lead_id(self, token: str) -> Optional[str]:
        """
        Decrypt the token to retrieve the original lead_id.
        
        Use this method when processing Jotform webhook submissions
        to recover the original lead_id from the encrypted token.
        
        Args:
            token: The encrypted token from the form submission
            
        Returns:
            Original lead_id or None if decryption fails
        """
        try:
            encrypted = base64.urlsafe_b64decode(token.encode())
            decrypted = self._fernet.decrypt(encrypted)
            lead_id = decrypted.decode()
            logger.debug(f"Successfully decrypted token to lead_id")
            return lead_id
        except Exception as e:
            logger.error(f"Failed to decrypt lead_id token: {e}")
            return None

    def get_form_url(self, lead_id: str) -> str:
        """
        Generate a dynamic Jotform URL with encrypted lead_id token as a URL parameter.
        
        The lead_id is encrypted to prevent exposure in URLs. Use this with a hidden
        field in your Jotform to securely track which submission came from which lead.
        
        When receiving the webhook submission, use decrypt_lead_id() to recover
        the original lead_id from the token.
        
        Args:
            lead_id: The lead ID to track (will be encrypted)
            
        Returns:
            Form URL with encrypted token as a query parameter
        """
        base_form_url = f"{self.base_url}/{self.form_id}"
        
        encrypted_token = self.encrypt_lead_id(lead_id)

        params = {"leadId": encrypted_token}
        url_with_params = f"{base_form_url}?{urllib.parse.urlencode(params)}"
        
        logger.debug(f"Generated Jotform URL for lead_id {lead_id} (encrypted)")
        return url_with_params
    
    def get_form_url_with_hidden_field(self, call_sid: str, hidden_field_id: str) -> str:
        """
        Generate form URL with call_sid as a hidden field value.
        Requires setting up a hidden field in your Jotform first.
        
        Args:
            call_sid: The call session ID to track
            hidden_field_id: The ID of the hidden field in your Jotform (e.g., "q3")
            
        Returns:
            Form URL with pre-filled hidden field
        """
        base_form_url = f"{self.base_url}/{self.form_id}"
        
        params = {hidden_field_id: call_sid}
        url_with_params = f"{base_form_url}?{urllib.parse.urlencode(params)}"
        
        logger.debug(f"Generated Jotform URL with hidden field for call_sid {call_sid}")
        return url_with_params
