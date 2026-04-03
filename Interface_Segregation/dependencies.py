from typing import Optional, Dict, Any
from twilio.rest import Client as TwilioClient
from twilio.request_validator import RequestValidator
from src.agents.factories.agent_factory import agent_factory
from src.services.call_session_service import CallSessionService
from src.config.settings import get_config
from src.utils.logger import logger
import threading

class ServiceLocator:
    """Centralized service locator for managing and providing access to various services used in the application."""
    
    _instance: Optional['ServiceLocator'] = None
    _instance_lock = threading.Lock()
    _init_lock = threading.Lock()

    def __new__(cls):
        if cls._instance is None:
            with cls._instance_lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if getattr(self, "_initialized", False):
            return
        
        with self._init_lock:
            if getattr(self, "_initialized", False):
                return
            
            self._initialize_services()
            self._initialized = True
    
    def _initialize_services(self) -> None:
        """Initialize all required services."""
        logger.info("Initializing ServiceLocator...")
        
        self.config = get_config()
        
        try:
            self.agent = agent_factory.create_swarm()
            logger.info("Single LangGraph agent initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize agent: {e}")
            raise RuntimeError(f"Agent initialization failed: {e}") from e
        
        self.twilio_client: Optional[TwilioClient] = None
        self.validator: Optional[RequestValidator] = None
        
        if self.config.twilio_account_sid and self.config.twilio_auth_token:
            try:
                self.twilio_client = TwilioClient(
                    self.config.twilio_account_sid,
                    self.config.twilio_auth_token
                )
                self.validator = RequestValidator(self.config.twilio_auth_token)
                logger.info("Twilio client and validator initialized")
            except Exception as e:
                logger.error(f"Failed to initialize Twilio client: {e}")
        else:
            logger.warning("Twilio credentials not configured")
        
        try:
            self.call_session_service = CallSessionService()
            logger.info("Call session service initialized")
        except Exception as e:
            logger.error(f"Failed to initialize call session service: {e}")
            self.call_session_service = None
        
        logger.info("ServiceLocator initialization completed")
    
    @property
    def is_twilio_configured(self) -> bool:
        """Check if Twilio is properly configured."""
        return (
            self.twilio_client is not None and
            self.validator is not None and
            bool(self.config.twilio_account_sid) and
            bool(self.config.twilio_auth_token)
        )
    
    @property
    def is_call_session_service_available(self) -> bool:
        """Check if call session service is available."""
        return self.call_session_service is not None
    
    def get_agent(self):
        """Get the LangGraph agent instance."""
        if self.agent is None:
            raise RuntimeError("Agent not initialized. Check initialization logs.")
        return self.agent

    def get_twilio_client(self) -> TwilioClient:
        """Get the Twilio client instance."""
        if self.twilio_client is None:
            raise RuntimeError("Twilio client not initialized. Ensure Twilio credentials are configured.")
        return self.twilio_client

    def get_twilio_validator(self) -> RequestValidator:
        """Get the Twilio request validator instance."""
        if self.validator is None:
            raise RuntimeError("Twilio request validator not initialized. Ensure Twilio credentials are configured.")
        return self.validator

    def get_call_session_service(self) -> CallSessionService:
        """Get the call session service instance."""
        if self.call_session_service is None:
            raise RuntimeError("Call session service not initialized.")
        return self.call_session_service

    def get_config(self):
        """Get the configuration instance."""
        if self.config is None:
            raise RuntimeError("Configuration not loaded.")
        return self.config
    
    def get_service_status(self) -> Dict[str, Any]:
        """Get status of all services."""
        return {
            "agent_initialized": self.agent is not None,
            "twilio_configured": self.is_twilio_configured,
            "call_session_service_available": self.is_call_session_service_available,
            "config_loaded": self.config is not None
        }
