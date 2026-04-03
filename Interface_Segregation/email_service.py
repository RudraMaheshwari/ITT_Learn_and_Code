import os
from pathlib import Path
import certifi
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, CustomArg, TrackingSettings, OpenTracking, ClickTracking
from src.email_automation.services.jotform_service import JotformService
from src.config.settings import get_config
from src.utils.logger import logger

os.environ["SSL_CERT_FILE"] = certifi.where()
config = get_config()

class EmailService:
    EMAIL_TEMPLATES = {
        "1": ("email_1_welcome.html", "Welcome to Our Platform, {name}!"),
        "2a": ("email_2a_deliverability.html", "Can you confirm you received our email?"),
        "2b": ("email_2b_holding_back.html", "What's holding you back, {name}?"),
        "3": ("email_3.html", "Quick reminder, {name}"),
        "4": ("email_4.html", "Special offer for you, {name}"),
        "5": ("email_5.html", "Success stories from our customers"),
        "6": ("email_6.html", "Last chance to join us, {name}"),
        "7": ("email_7.html", "Final follow-up, {name}"),
    }

    def __init__(
        self,
        api_key: str | None = None,
        from_email: str | None = None,
    ) -> None:
        """
        Email service wrapper around SendGrid.
        Values can be injected or taken from settings.
        """
        self.api_key = api_key or config.sendgrid_api_key
        self.from_email = from_email or config.sendgrid_from_email

        if not self.api_key:
            raise ValueError("SENDGRID_API_KEY is not set.")
        if not self.from_email:
            raise ValueError("SENDER_EMAIL is not set.")

        self._client = SendGridAPIClient(self.api_key)
        try:
            self.jotform_service = JotformService()
        except ValueError:
            logger.warning("Jotform service not configured. JOTFORM_FORM_ID not set.")
            self.jotform_service = None

    def _get_template_path(self) -> Path:
        """Get the path to email templates directory."""
        return Path(__file__).parent.parent / "email_templates"

    def _load_email_template(self, email_sequence_number: str, lead_name: str, jotform_url: str) -> tuple[str, str]:
        """
        Load HTML email template based on sequence number.
        Returns (subject, html_content) tuple.
        """
        if email_sequence_number not in self.EMAIL_TEMPLATES:
            raise ValueError(f"Invalid email sequence number: {email_sequence_number}")
        
        template_filename, subject_template = self.EMAIL_TEMPLATES[email_sequence_number]
        template_path = self._get_template_path() / template_filename
        
        if not template_path.exists():
            raise FileNotFoundError(f"Email template not found: {template_path}")
        
        with open(template_path, "r", encoding="utf-8") as f:
            html_template = f.read()
        
        html_content = html_template.format(
            name=lead_name,
            jotform_url=jotform_url,
        )
        subject = subject_template.format(name=lead_name)
        
        return subject, html_content

    def send_email(self, message: Mail) -> None:
        """
        Low-level helper to send a prepared SendGrid Mail object.
        Returns response object with message_id extracted from headers.
        """
        try:
            response = self._client.send(message)
            logger.info("Email sent. Status: %s", response.status_code)
            logger.debug("Email response body: %s", response.body)
            logger.debug("Email response headers: %s", response.headers)
            
            message_id = None
            if response.headers:
                message_id = response.headers.get("X-Message-Id")
                if not message_id:
                    for key, value in response.headers.items():
                        if key.lower() == "x-message-id":
                            message_id = value
                            break
            
            if message_id:
                response.message_id = message_id
                logger.debug(f"Extracted message ID: {message_id}")
            
            return response
        except Exception as exc:
            logger.exception("Failed to send email: %s", exc)
            return None

    def send_email_sequence(self, to_email: str, lead_name: str, lead_id: str, email_sequence_number: str) -> None:
        """
        Send email to lead based on sequence number.
        Uses HTML templates from email_templates directory.
        
        Args:
            to_email: Recipient email address
            lead_name: Name of the lead for personalization
            lead_id: Unique lead identifier for tracking
            email_sequence_number: Template identifier ("1", "2a", "2b", "3", "4", "5", "6", or "7")
        """
        if self.jotform_service:
            jotform_url = self.jotform_service.get_form_url(lead_id)
        else:
            jotform_url = "#"
            logger.warning("Using static JOTFORM_URL. Dynamic tracking with lead_id not available.")

        subject, html_content = self._load_email_template(email_sequence_number, lead_name, jotform_url)

        message = Mail(
            from_email=self.from_email,
            to_emails=to_email,
            subject=subject,
            html_content=html_content,
        )

        message.custom_arg = [
            CustomArg(key="lead_id", value=lead_id)
        ]
        message.tracking_settings = TrackingSettings()
        message.tracking_settings.open_tracking = OpenTracking(enable=True)
        message.tracking_settings.click_tracking = ClickTracking(enable=True, enable_text=False)
        
        response = self.send_email(message)
        logger.info(f"Email sequence {email_sequence_number} sent successfully")
        return response

_email_service = None

def get_email_service() -> EmailService:
    """Singleton factory for EmailService."""
    global _email_service
    if _email_service is None:
        _email_service = EmailService()
    return _email_service
