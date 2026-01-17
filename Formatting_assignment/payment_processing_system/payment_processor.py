from decimal import Decimal
from datetime import datetime
from typing import Dict
from exceptions import PaymentException
from models import PaymentResult, PaymentRecord, PaymentRequest
from services import Logger, NotificationService

class PaymentProcessor:
    """Payment processor for handling payment transactions."""
    
    MIN_AMOUNT = Decimal("0.01")
    MAX_PAYMENT_AMOUNT = Decimal("5000")
    MAX_RETRIES = 2
    PAYMENT_SUCCESS = "Payment successful"
    PAYMENT_FAILED = "Payment failed"
    INITIAL_ATTEMPT = 0
    TIMESTAMP_MULTIPLIER = 1000

    def __init__(self, logger: Logger, notifier: NotificationService) -> None:
        """Initialize the payment processor."""
        self.logger = logger
        self.notifier = notifier
        self.history: Dict[str, PaymentRecord] = {}

    def process(self, request: PaymentRequest) -> PaymentResult:
        """Process a payment request."""
        self._validate(request)
        
        attempt = self.INITIAL_ATTEMPT
        while attempt < self.MAX_RETRIES:
            try:
                self._execute(request)
                self._record(request)
                self._notify_success(request)
                return PaymentResult(True, self.PAYMENT_SUCCESS, self._generate_id())
            except PaymentException:
                attempt += 1
                self.logger.log(f"Retry attempt: {attempt}")
        
        return PaymentResult(False, self.PAYMENT_FAILED, None)

    def _validate(self, request: PaymentRequest) -> None:
        """Validate the payment request."""
        if not request.customer_id or not request.customer_id.strip():
            raise ValueError("Customer ID required")
        
        if not request.amount or request.amount < self.MIN_AMOUNT:
            raise ValueError("Invalid amount")

    def _execute(self, request: PaymentRequest) -> None:
        """Execute the payment."""
        self.logger.log(f"Executing payment of {request.amount}")
        
        if request.amount > self.MAX_PAYMENT_AMOUNT:
            raise PaymentException("Limit exceeded")

    def _record(self, request: PaymentRequest) -> None:
        """Record the payment in history."""
        self.history[self._generate_id()] = PaymentRecord(
            request.customer_id,
            request.amount,
            datetime.now()
        )

    def _notify_success(self, request: PaymentRequest) -> None:
        """Notify customer of successful payment."""
        self.notifier.send(request.customer_id, f"Payment of {request.amount} processed")

    def _generate_id(self) -> str:
        """Generate a unique transaction ID."""
        return f"TXN-{int(datetime.now().timestamp() * self.TIMESTAMP_MULTIPLIER)}"
